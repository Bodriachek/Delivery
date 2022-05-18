from django_filters import rest_framework as filters
from .models import Order, Fueling, Car, Manager, Driver


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class OrderFilter(filters.FilterSet):
    # Фільтр, для відображення замовлень конкретного водія з різними статусами
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['driver', 'date_trip']


class RefuelingListFilter(filters.FilterSet):
    class Meta:
        model = Fueling
        fields = ['driver', 'created']


class DriversListFilter(filters.FilterSet):

    class Meta:
        model = Driver
        fields = ['orders__car', 'orders__manager']


class ManagerListFilter(filters.FilterSet):

    class Meta:
        model = Manager
        fields = ['orders__driver']


class CarsListFilter(filters.FilterSet):
    load_capacity = filters.RangeFilter()
    width_trunk = filters.RangeFilter()
    length_trunk = filters.RangeFilter()
    height_trunk = filters.RangeFilter()

    class Meta:
        model = Car
        fields = ['load_capacity', 'width_trunk', 'length_trunk', 'height_trunk']
