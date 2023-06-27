from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Check unique email
    # Email exists && app_account active -> email_already_registered
    # Email exists && app_account not active -> delete previous app_account and register new one
    def clean_email(self):
        email_passed = self.cleaned_data.get("email")
        email_already_registered = User.objects.filter(email=email_passed).exists()
        user_is_active = User.objects.filter(email=email_passed, is_active=1)
        if email_already_registered and user_is_active:
            raise forms.ValidationError("Este correo ya está registrado.")
        # elif email_already_registered:
        #     User.objects.filter(email=email_passed).delete()

        return email_passed
