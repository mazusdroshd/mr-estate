from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from account.serializers import PhoneSerializer
from account.utils.otp import TOTP
from account.utils.exeptions import UserExists, TooEarly


class RequestOtpView(APIView):
    http_method_names = ['post', ]
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            totp = TOTP(phone_number=serializer.validated_data['phone_number'])
            try:
                code = totp.generate_otp()
                totp.send_otp(code)
                return Response({'detail': 'code sent successfully'})
            except UserExists:
                return Response({'detail': 'user with this phone number exists'}, status=status.HTTP_400_BAD_REQUEST)
            except TooEarly as error:
                return Response({'detail': error.msg, 'remaining_time': error.remaining_seconds}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors)
