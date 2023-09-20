import django_filters

from .models import Advertise


class AdvertiseFilter(django_filters.FilterSet):
    min_date = django_filters.DateFilter(
        field_name='created', lookup_expr='gte')
    max_date = django_filters.DateFilter(
        field_name='created', lookup_expr='lte')
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte')
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains')
    address = django_filters.CharFilter(
        field_name='user', lookup_expr='address__icontains'
    )

    class Meta:
        model = Advertise
        fields = [
            'min_date',
            'max_date',
            'min_price',
            'max_price',
            'title',
            'address',
        ]
