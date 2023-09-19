from django.db import models
from django.contrib.auth.models import AbstractUser

from account.validators import phone_validator
from account.managers import CustomUserManager


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_validator,]
    )
    address = models.TextField(blank=False)
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "address",]

    def __str__(self) -> str:
        return self.get_full_name()
