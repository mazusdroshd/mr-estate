from django.urls import path

from advertise import views

app_name = 'advertise'

urlpatterns = [
    path('', views.AdvertiseListView.as_view(), name='ads_list'),
]
