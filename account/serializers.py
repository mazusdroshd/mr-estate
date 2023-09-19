from rest_framework import serializers

from account.validators import phone_validator


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        phone_validator(value)
        return value
