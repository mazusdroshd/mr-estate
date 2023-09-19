from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account import views


app_name = 'account'

urlpatterns = [
    path('request_otp/', views.RequestOtpView.as_view(), name='request_otp'),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
