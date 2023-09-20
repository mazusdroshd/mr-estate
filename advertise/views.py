import django_filters

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.db import transaction

from advertise.models import Advertise
from advertise.serializers import AdvertiseListSerializer, AdvertiseSerializer, AdvertiseImageSerializer
from advertise.filters import AdvertiseFilter
from advertise.permissions import IsImageOwner, IsOwnerOrReadOnly


class AdvertiseListViewSet(viewsets.ModelViewSet):
    queryset = Advertise.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, ]
    filterset_class = AdvertiseFilter
    ordering_fields = ['created', 'price']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 30
    permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        with transaction.atomic():
            advertise = serializer.save(user=self.request.user)
            files = self.request.FILES.getlist('images')

            if not files:
                raise ValidationError(
                    {'images': 'this field is required'})

            if len(files) > 3:
                raise ValidationError(
                    {'error': 'you can not upload more than 3 images'})

            for file in files:
                image_serializer = AdvertiseImageSerializer(
                    data={'image': file})
                if image_serializer.is_valid():
                    image_serializer.save(advertise=advertise)
                else:
                    raise ValidationError(
                        {'error': 'image sent is not valid'})

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            return AdvertiseListSerializer(*args, **kwargs)

        serailizer = AdvertiseSerializer(*args, **kwargs)
        if self.action in ['update', 'partial_update', 'create']:
            serailizer.fields['images'].read_only = True

        return serailizer

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering')

        if ordering in self.ordering_fields:
            queryset = queryset.order_by(ordering)

        return queryset
