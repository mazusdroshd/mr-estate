from django.urls import path, include
from rest_framework.routers import DefaultRouter

from advertise import views

app_name = 'advertise'

router = DefaultRouter()
router.register('', views.AdvertiseViewSet, basename='advertise')

urlpatterns = [
    path('', include(router.urls)),
    path('upload_image/<int:pk>/',
         views.CreateImageView.as_view(), name="upload_image"),
    path('delete_image/<int:pk>/',
         views.DeleteImageView.as_view(), name="delete_image"),
]
