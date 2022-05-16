from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, viewsets, generics
from .serializers import (
    CreateOrderSerializer, FuelingSerializer, DriverListSerializer, ManagerListSerializer,
    CarListSerializer, ChangeOrderSerializer, AddFuelingSerializer, RepairListSerializer, AddRepairSerializer,
    DriverSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .service import OrderFilter, RefuelingListFilter, DriversListFilter, ManagerListFilter, CarsListFilter
from .models import Order, Fueling, Car, Repair, Driver


class CreateOrderView(generics.CreateAPIView):
    """ Add order for customer """
    queryset = Order.objects.filter(status=Order.STATUS_NEW)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateOrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ Change order, for staff """
    queryset = Order.objects.filter(status=Order.STATUS_PREPARE_TO_SHIP)
    permission_classes = [permissions.AllowAny]
    serializer_class = ChangeOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter


class DriverListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.filter(status=Order.STATUS_DONE)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DriverListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriversListFilter


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.filter(
        Q(status=Order.STATUS_PREPARE_TO_SHIP) |
        Q(status=Order.STATUS_DONE)
    )
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ManagerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManagerListFilter


class FuelingViewSet(viewsets.ReadOnlyModelViewSet):
    """Реєстрація та список заправок"""
    queryset = Fueling.objects.filter(created__lte=timezone.now())
    permission_classes = [permissions.IsAdminUser]
    serializer_class = FuelingSerializer
    filter_backends = (DjangoFilterBackend,)
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


class AddRepairView(generics.CreateAPIView):
    """ Ремонти """
    queryset = Repair.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AddRepairSerializer


class CarsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Car.objects.filter(is_repair=False).order_by('load_capacity')
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CarListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarsListFilter


