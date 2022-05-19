from django.db.models import Q, Sum, Case, When
from django.utils import timezone
from rest_framework import permissions, viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreateOrderSerializer, FuelingSerializer, DriverListSerializer, ManagerListSerializer,
    ShortCarListSerializer, OrderListSerializer, AddFuelingSerializer, RepairListSerializer, AddRepairSerializer,
    DriverSerializer, AddDriverSerializer, StaffOrderSerializer, CarListSerializer, CarSizeSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .service import OrderFilter, RefuelingListFilter, DriversListFilter, ManagerListFilter
from .models import Order, Fueling, Car, Repair, Driver, Manager


class StaffOrderView(viewsets.ModelViewSet):
    """ CRUD order for staff """
    queryset = Order.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = StaffOrderSerializer


class AddOrderView(generics.CreateAPIView):
    """ Add order for customer """
    queryset = Order.objects.filter(status=Order.STATUS_NEW)
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateOrderSerializer


class OrderListViewSet(viewsets.ModelViewSet):
    """ Change order, for staff """
    queryset = Order.objects.filter(status=Order.STATUS_PREPARE_TO_SHIP)
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter


class DriverListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Driver.objects.distinct()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = DriverListSerializer

    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = DriversListFilter

    def get_queryset(self):
        sort_mileage = sorted(self.queryset, key=lambda d: float(d.mileage))
        return sort_mileage

    def get(self, request, *args, **kwargs):
        sort_mileage = list()
        # product_weight = self.request.query_params.get('product_weight', None)
        # product_width = self.request.query_params.get('product_width', None)
        # product_length = self.request.query_params.get('product_length', None)
        # product_height = self.request.query_params.get('product_height', None)

        for orders__car in Driver.objects.filter(orders__status=Order.STATUS_DONE):
            if driver__orders__car == orders__car:
                sort_mileage.append(driver__orders__car)

        data = DriverListSerializer(sort_mileage, many=True).data


class ManagerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Manager.objects.distinct()
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


class CarsListAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        necessary_cars = list()
        product_weight = self.request.query_params.get('product_weight', None)
        product_width = self.request.query_params.get('product_width', None)
        product_length = self.request.query_params.get('product_length', None)
        product_height = self.request.query_params.get('product_height', None)

        for car in Car.objects.filter(load_capacity__gte=int(product_weight)):
            if car.dimensions >= sorted([int(product_width), int(product_length), int(product_height)]):
                necessary_cars.append(car)

        data = CarSizeSerializer(necessary_cars, many=True).data

        return Response(data)
