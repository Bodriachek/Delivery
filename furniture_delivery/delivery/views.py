from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, viewsets, generics
from rest_framework.filters import OrderingFilter

from .serializers import (
    CreateOrderSerializer, FuelingSerializer, DriverListSerializer, ManagerListSerializer,
    ShortCarListSerializer, OrderSerializer, AddFuelingSerializer, RepairListSerializer, AddRepairSerializer,
    DriverSerializer, AddDriverSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .service import OrderFilter, RefuelingListFilter, DriversListFilter, ManagerListFilter, CarsListFilter
from .models import Order, Fueling, Car, Repair, Driver, Manager


class CreateOrderView(generics.CreateAPIView):
    """ Add order for customer """
    queryset = Order.objects.filter(status=Order.STATUS_NEW)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateOrderSerializer


class OrderListViewSet(viewsets.ModelViewSet):
    """ Change order, for staff """
    queryset = Order.objects.filter(status=Order.STATUS_PREPARE_TO_SHIP)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter


class DriverListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Driver.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DriverListSerializer
    filter_backends = (DjangoFilterBackend)
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = DriversListFilter
    # ordering_fields = ['mileage']


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manager.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ManagerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManagerListFilter


class FuelingViewSet(viewsets.ReadOnlyModelViewSet):
    """Реєстрація та список заправок"""
    queryset = Fueling.objects.filter(created__lte=timezone.now())
    permission_classes = [permissions.IsAdminUser]
    serializer_class = FuelingSerializer
    filter_backends = (DjangoFilterBackend)
    filterset_class = RefuelingListFilter


class AddFuelingView(generics.CreateAPIView):
    """Реєстрація та список заправок"""
    queryset = Fueling.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AddFuelingSerializer


class RepairsViewSet(viewsets.ReadOnlyModelViewSet):
    """ Ремонти """
    queryset = Repair.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RepairListSerializer


class DriverCarRepairViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Driver.objects.filter(car__is_repair=True)
    permissions_classes = [permissions.IsAdminUser]
    serializer_class = DriverSerializer


class AddDriverView(generics.CreateAPIView):
    queryset = Driver.objects.all()
    permissions_classes = [permissions.IsAdminUser]
    serializer_class = AddDriverSerializer


class AddRepairView(generics.CreateAPIView):
    """ Ремонти """
    queryset = Repair.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AddRepairSerializer


class CarsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.filter(is_repair=False).order_by('load_capacity')
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ShortCarListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarsListFilter


