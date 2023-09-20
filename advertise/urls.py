from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertise import views

app_name = 'advertise'

router = DefaultRouter()
router.register('', views.AdvertiseListViewSet, basename='advertise')

urlpatterns = [
    path('', include(router.urls)),
]
