from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number: str, first_name: str, last_name: str, address: str, password: str = None):
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number: str, first_name: str, last_name: str, address: str, password: str = None):
        user = self.create_user(
            phone_number=phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            address=address,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
