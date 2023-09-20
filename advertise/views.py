from rest_framework import generics

from advertise.models import Advertise
from advertise.serializers import AdvertiseListSerializer


class AdvertiseListView(generics.ListAPIView):
    serializer_class = AdvertiseListSerializer
    queryset = Advertise.objects.all()
