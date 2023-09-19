import pyotp

from datetime import datetime, timedelta
from django.core.cache import cache
from django.contrib.auth import get_user_model

from account.utils.exeptions import TooEarly, UserExists


class TOTP:
    def __init__(self, phone_number: str) -> None:
        self.phone_number = phone_number

    def generate_otp(self) -> str:
        user_model = get_user_model()
        if user_model.objects.filter(phone_number=self.phone_number).exists():
            raise UserExists()

        last_request_time = cache.get(f"{self.phone_number}_request_time")
        if last_request_time:
            elapsed_time = datetime.now() - last_request_time
            if elapsed_time < timedelta(minutes=1):
                remaining_seconds = 60 - elapsed_time.seconds
                raise TooEarly(
                    "Please wait at least one minute before requesting another OTP.", remaining_seconds
                )

        secret = pyotp.random_base32()
        cache.set(self.phone_number, secret, timeout=60*5)
        cache.set(f"{self.phone_number}_request_time",
                  datetime.now(), timeout=60)
        totp = pyotp.TOTP(secret, interval=60*5)
        otp = totp.now()
        return otp

    def validate_otp(self, code) -> bool:
        secret = cache.get(self.phone_number)
        if secret:
            totp = pyotp.TOTP(secret, interval=5*60)
            return totp.verify(code)
        return False

    def send_otp(self, code):
        print(f"{self.phone_number} -> {code}")
