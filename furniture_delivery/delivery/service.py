from django_filters import rest_framework as filters
from .models import Order, Fueling, Car


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
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['car', 'manager', 'date_trip']


class ManagerListFilter(filters.FilterSet):
    date_trip = filters.DateRangeFilter()

    class Meta:
        model = Order
        fields = ['driver', 'date_trip']


class CarsListFilter(filters.FilterSet):
    load_capacity = filters.RangeFilter()
    width_trunk = filters.RangeFilter()
    length_trunk = filters.RangeFilter()
    height_trunk = filters.RangeFilter()


    class Meta:
        model = Car
        fields = ['load_capacity', 'width_trunk', 'length_trunk', 'height_trunk']
