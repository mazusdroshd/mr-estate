from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from account.serializers import UserSerializer, VerifyUserSerializer, UserUpdateSerializers
from account.utils.otp import TOTP
from account.utils.exeptions import UserExists, TooEarly


class CreateUserView(APIView):
    serializer_class = UserSerializer
    http_method_names = ['post',]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_model = get_user_model()
        phone_number = request.data.get('phone_number')
        password = serializer.validated_data.get('password')
        user = user_model.objects.filter(
            phone_number=phone_number).first()
        totp = TOTP()
        if not user:
            user = user_model.objects.create(
                phone_number=phone_number,
            )
        user.set_password(password)
        user.save()

        try:
            code = totp.generate_otp(user=user)
        except UserExists:
            return Response({'error': 'user with this phone number exists'}, status=status.HTTP_400_BAD_REQUEST)
        except TooEarly as error:
            return Response({
                'error': error.msg,
                'remaining_time': error.remaining_seconds,
            }, status=status.HTTP_425_TOO_EARLY)
        totp.send_otp(user, code)
        return Response(serializer.data)


class VerifyUserView(APIView):
    serializer_class = VerifyUserSerializer
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        totp = TOTP()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']
        user_model = get_user_model()
        try:
            user = user_model.objects.get(phone_number=phone_number)
        except user_model.DoesNotExist:
            return Response({'error': 'user with this phone number doesn\'t exists'}, status=status.HTTP_400_BAD_REQUEST)

        if totp.validate_otp(user=user, code=code):
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'code is not valid'}, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializers
    permission_classes = [permissions.IsAuthenticated, ]

    def get_object(self):
        return self.request.user
