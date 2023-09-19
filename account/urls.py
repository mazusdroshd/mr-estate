from django.urls import path

from account import views


app_name = 'account'

urlpatterns = [
    path('request_otp/', views.RequestOtpView.as_view(), name='request_otp'),
    path('signup/', views.CreateUserView.as_view(), name='signup'),
]
