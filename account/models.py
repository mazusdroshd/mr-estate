from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from account.validators import phone_validator
from account.managers import CustomUserManager


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_validator,]
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    address = models.TextField(blank=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    def __str__(self) -> str:
        return self.get_full_name()
