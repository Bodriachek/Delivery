from django_filters import rest_framework as filters
from .models import Order, Fueling, Manager, Driver


class OrderFilter(filters.FilterSet):
    # Фільтр, для відображення замовлень конкретного водія з різними статусами
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['driver', 'date_trip']


class RefuelingListFilter(filters.FilterSet):
    created = filters.DateRangeFilter()

    class Meta:
        model = Fueling
        fields = ['car', 'car__driver', 'created']


class DriversListFilter(filters.FilterSet):

    class Meta:
        model = Driver
        fields = ['orders__car', 'orders__manager']


class ManagerListFilter(filters.FilterSet):

    class Meta:
        model = Manager
        fields = ['orders__driver']
