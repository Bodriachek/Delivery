from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import permissions, viewsets, generics
from .models import Order, Fueling, Car, Repair, Driver, Manager
from .permissions import IsSuperUser, IsAdminOrReadOnly
from .serializers import (
    CreateOrderSerializer, FuelingSerializer, DriverListSerializer, ManagerListSerializer,
    FutureOrderListSerializer, AddFuelingSerializer, RepairListSerializer, AddRepairSerializer,
    DriverSerializer, StaffOrderSerializer, CarSizeSerializer
)
from .service import OrderFilter, RefuelingListFilter, ManagerListFilter


class StaffOrderView(viewsets.ModelViewSet):
    """ CRUD order for staff """
    queryset = Order.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = StaffOrderSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(driver__user=self.request.user) | Q(manager__user=self.request.user)
            )


class FutureOrderListView(generics.ListAPIView):
    """ Change order, for staff """
    queryset = Order.objects.filter(status=Order.STATUS_PREPARE_TO_SHIP)
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FutureOrderListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class AddOrderView(generics.CreateAPIView):
    """ Add order for customer """
    queryset = Order.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateOrderSerializer


class DriverListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsSuperUser]
    serializer_class = DriverListSerializer

    def get_queryset(self):
        driver_list = list()

        query_params = self.request.query_params

        manager = query_params.get('manager')
        car = query_params.get('car')

        for driver in Driver.objects.filter(
                (Q(orders__status=Order.STATUS_DONE)) &
                (Q(orders__manager=manager) | Q(orders__car=car))).distinct():
            driver_list.append(driver)

        sort_mileage = sorted(driver_list, key=lambda driver: float(driver.mileage))
        return sort_mileage


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manager.objects.distinct()
    permission_classes = [IsSuperUser]
    serializer_class = ManagerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManagerListFilter


class FuelingViewSet(viewsets.ReadOnlyModelViewSet):
    """Список заправок"""
    queryset = Fueling.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FuelingSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RefuelingListFilter

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class AddFuelingView(generics.CreateAPIView):
    """Реєстрація та список заправок"""
    queryset = Fueling.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddFuelingSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class RepairsViewSet(viewsets.ReadOnlyModelViewSet):
    """ Ремонти """
    queryset = Repair.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RepairListSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class DriverCarRepairViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Driver.objects.filter(car__is_repair=True)
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = DriverSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_staff:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class AddRepairView(generics.CreateAPIView):
    """ Ремонти """
    queryset = Repair.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddRepairSerializer

    def get_queryset(self):
        """Return object for current authenticated user only"""
        if self.request.user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(
                Q(car__driver__user=self.request.user)
            )


class CarsListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CarSizeSerializer

    def get_queryset(self):
        necessary_cars = list()

        query_params = self.request.query_params

        product_weight = query_params.get('product_weight')
        product_width = query_params.get('product_width')
        product_length = query_params.get('product_length')
        product_height = query_params.get('product_height')

        for car in Car.objects.filter(
                Q(load_capacity__gte=int(product_weight)) & Q(is_repair=False)).distinct():
            if car.dimensions >= sorted([int(product_width), int(product_length), int(product_height)]):
                necessary_cars.append(car)

        sort_load_capacity = sorted(necessary_cars, key=lambda car: float(car.load_capacity))
        return sort_load_capacity
