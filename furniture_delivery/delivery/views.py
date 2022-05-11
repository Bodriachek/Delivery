from datetime import datetime

from django.db import models
from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateOrderSerializer, OrderListSerializer, RegisterRefuelingSerializer, \
    RefuelingListSerializer, AddRepairSerializer, RepairsSerializer, DriverListSerializer, ManagerListSerializer, \
    CarListSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .service import OrderFilter, RefuelingListFilter, DriversListFilter, ManagerListFilter, CarsListFilter
from .models import Order, RegistrationRefueling, Cars, Driver


class OrderViewSet(viewsets.ModelViewSet):
    """ Список та створення замовлень """
    queryset = Order.objects.filter(
        Q(status=2) |
        Q(status=3)
    )
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return CreateOrderSerializer
        elif self.action == 'update':
            return OrderListSerializer
        elif self.action == 'create':
            return CreateOrderSerializer


class RefuelingViewSet(viewsets.ModelViewSet):
    """Реєстрація та список заправок"""
    queryset = RegistrationRefueling.objects.filter(date_refueling__lte=datetime.now())
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RefuelingListFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return RefuelingListSerializer
        elif self.action == 'retrieve':
            return RegisterRefuelingSerializer
        elif self.action == 'create':
            return RegisterRefuelingSerializer


class RepairsViewSet(viewsets.ModelViewSet):
    """ Ремонти """
    permission_classes = [permissions.IsAdminUser]
    queryset = Cars.objects.filter(is_repair=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return RepairsSerializer
        elif self.action == 'retrieve':
            return AddRepairSerializer
        elif self.action == 'create':
            return AddRepairSerializer


class DriversViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.filter(status=4)
        # .order_by('driver__mileage')
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DriverListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = DriversListFilter


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.filter(
        Q(status=3) |
        Q(status=4)
    )
    permission_classes = [permissions.IsAdminUser]
    serializer_class = ManagerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ManagerListFilter


class CarsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cars.objects.filter(is_repair=False).order_by('load_capacity')
    permission_classes = [permissions.IsAdminUser]
    serializer_class = CarListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarsListFilter


class DriversListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cars.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DriverListSerializer

