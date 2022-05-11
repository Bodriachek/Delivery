from django.db import transaction
from django_filters import rest_framework as filters
from .models import Order, RegistrationRefueling, Cars, Driver


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class OrderFilter(filters.FilterSet):
    # Фільтр, для відображення замовлень конкретного водія з різними статусами
    driver = filters.BaseInFilter(field_name='driver__name')
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['driver', 'date_trip']


class RefuelingListFilter(filters.FilterSet):
    driver = filters.BaseInFilter(field_name='driver__name')
    date_refueling = filters.DateRangeFilter()

    class Meta:
        model = RegistrationRefueling
        fields = ['driver', 'date_refueling']


class DriversListFilter(filters.FilterSet):
    car = filters.BaseInFilter(field_name='car__title')
    manager = filters.BaseInFilter(field_name='manager__name')
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['car', 'manager', 'date_trip']


class ManagerListFilter(filters.FilterSet):
    driver = filters.BaseInFilter(field_name='driver__name')
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['driver', 'date_trip']


class CarsListFilter(filters.FilterSet):
    load_capacity = filters.RangeFilter()
    width = filters.RangeFilter()
    length = filters.RangeFilter()
    height = filters.RangeFilter()


    class Meta:
        model = Cars
        fields = ['load_capacity', 'width', 'length', 'height']
