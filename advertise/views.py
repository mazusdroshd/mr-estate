import django_filters

from rest_framework import generics

from advertise.models import Advertise
from advertise.serializers import AdvertiseListSerializer
from advertise.filters import AdvertiseFilter


class AdvertiseListView(generics.ListAPIView):
    serializer_class = AdvertiseListSerializer
    queryset = Advertise.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = AdvertiseFilter
    ordering_fields = ['created', 'price']
