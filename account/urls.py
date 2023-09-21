from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account import views


app_name = 'account'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('verify/', views.VerifyUserView.as_view(), name='verify_user'),
    path('user/', views.UserRetrieveUpdateView.as_view(), name="user_info"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
