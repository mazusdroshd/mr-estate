from rest_framework import serializers

from account.validators import phone_validator
from account.models import CustomUser
from account.utils.otp import TOTP


class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)

    def validate_phone_number(self, value):
        phone_validator(value)
        return value


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        del validated_data['confirm_password']
        del validated_data['code']
        return CustomUser.objects.create_user(**validated_data)

    def validate(self, data):
        password = data['password']
        confirm_password = data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError(
                'password and confirm password doesn\'t match.')

        phone_number = data['phone_number']
        code = data['code']
        otp = TOTP(phone_number)
        if not otp.validate_otp(code):
            raise serializers.ValidationError('code is not valid.')

        return data

    class Meta:
        model = CustomUser
        fields = ['phone_number',
                  'first_name',
                  'last_name',
                  'address',
                  'password',
                  'confirm_password',
                  'code'
                  ]
