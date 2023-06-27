from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from app_account.forms import RegisterUserForm
# from app_core.models import Config
from mieles.utils import create_mail

UserModel = get_user_model()


def get_host_url(request) -> str:
    if request.get_host().__contains__("127.0.0.1") or request.get_host().__contains__(
            "localhost"):
        host = 'http://'
    else:
        host = 'https://'
    # host += request.get_host() + '/'
    return host


def register(request):
    if request.user.is_authenticated:
        print('Already authenticated')
        return HttpResponseRedirect('/admin/')
    else:
        if request.method == 'POST':
            form = RegisterUserForm(request.POST)
            # RegisterUserForm is created from User model, all model field restrictions are checked to considerate it
            # a valid form
            if form.is_valid():
                print('Valid form')
                # Save user to database but with is_active = False
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                # Send confirmation email
                # from apps.core.models import Config
                current_site = get_current_site(request)
                subject = 'Activa tu ' + current_site.domain + ' cuenta'
                to_email = form.cleaned_data.get('email')
                # message = render_to_string('registration/confirmation_mail.html', {
                #     'host': get_host_url(request),
                #     "domain": current_site.domain,
                #     "user": user,
                #     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                #     "token": default_token_generator.make_token(user),
                #     'cfg': Config.objects.first() if Config.objects.exists() else None
                # }, )
                # send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email])

                mail = create_mail(to_email, subject, 'registration/confirmation_mail.html', {
                    'host': get_host_url(request),
                    "domain": current_site.domain,
                    "user": user,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                    # 'cfg': Config.objects.first() if Config.objects.exists() else None
                })
                mail.send(fail_silently=False)

                # Redirect user to login

                messages.success(request,
                                 'Por favor confirma su email para completar el registro antes de iniciar sesión.')
                return HttpResponseRedirect(reverse('login'))
            else:
                print('Invalid form: %s' % form.errors.as_data())
                print(type(form.errors.as_data()))
                if form.errors:
                    messages.info(request, 'Errores en el formulario')
                    for key, values in form.errors.as_data().items():
                        print("Bad value: %s - %s" % (key, values))
                        if key == 'username':
                            messages.info(request, 'Error input fields')
                            break
                        else:
                            for error_value in values:
                                print(error_value)
                                # print(type(error_value))
                                messages.info(request, '%s' % error_value.message)

                # return HttpResponseRedirect(reverse('usersAuth:register'))
                return render(request, 'registration/register.html',
                              {'form': form, 'messages': messages.get_messages(request)})
        else:
            form = RegisterUserForm()

            context = {'form': form}
            return render(request, 'registration/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect user to login
        messages.success(request, 'Su email se ha confirmado, puede proceder a autenticarse')
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'registration/fail_confirmation.html',
                      {'message': 'El link de activación es invalido o ha expirado'},
                      status=403)


class MyPasswordResetView(PasswordResetView):
    email_template_name = "registration/password_reset_mail.html"
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = "registration/password_reset_mail.html"
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        # self.extra_email_context = {'cfg': Config.objects.first() if Config.objects.exists() else None}
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context.update({'cfg': Config.objects.first() if Config.objects.exists() else None})
        return context

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)
