from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    is_superstar = models.BooleanField(
        _("Admin"), default=False, help_text=_("Designates that this user has all permissions without "
                                               "explicitly assigning them."), )
    is_superuser = models.BooleanField(
        _("superuser status"), default=True, help_text=_(
            "Designates that this user has all permissions without "
            "explicitly assigning them."
        ), )
    is_staff = models.BooleanField(
        _("staff status"), default=True, help_text=_("Designates whether the user can log into this admin site."), )
    REQUIRED_FIELDS = ['is_superstar', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Usuario'
        ordering = ('-is_superstar', '-is_active')

    def __str__(self):
        return self.username
