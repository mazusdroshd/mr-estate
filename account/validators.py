from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r"^09\d{9}$", message="Phone number must be in the format 09xxxxxxxxx."
)
