from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager')


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')

    DRIVER_CLASS_B = 1
    DRIVER_CLASS_CHOICES = (
        (DRIVER_CLASS_B, 'B'),
        (2, 'C1'),
        (3, 'C'),
    )
    driver_class = MultiSelectField(choices=DRIVER_CLASS_CHOICES, default=DRIVER_CLASS_B)

    @property
    def mileage(self):
        distances = self.orders.filter(status=Order.STATUS_DONE).values_list('total_distance', flat=True)
        return sum(distances)

    @property
    def dates_future_orders(self):
        dates_trips = self.orders.filter(status=Order.STATUS_PREPARE_TO_SHIP).values_list('date_trip', flat=True)
        return dates_trips


class Car(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    state_number = models.CharField(max_length=10, null=True)
    driver_class = models.PositiveIntegerField(choices=Driver.DRIVER_CLASS_CHOICES, default=Driver.DRIVER_CLASS_B)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    load_capacity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In kilograms'
    )
    width_trunk = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In meters'
    )
    length_trunk = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In meters'
    )
    height_trunk = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In meters'
    )

    # ПАЛИВО
    GASOLINE = 1
    DIESEL = 2
    GAS = 3

    TYPE_OF_FUEL_CHOICES = (
        (GASOLINE, 'GASOLINE'),
        (DIESEL, 'DIESEL'),
        (GAS, 'GAS'),
    )

    type_fuel = models.PositiveSmallIntegerField(choices=TYPE_OF_FUEL_CHOICES)
    tank_size = models.PositiveSmallIntegerField(help_text='In liters')
    fuel_consumption = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    # РЕМОНТ
    is_repair = models.BooleanField(default=False)

    @property
    def dates_future_orders(self):
        dates_trips = self.orders.filter(status=Order.STATUS_PREPARE_TO_SHIP).values_list('date_trip', flat=True)
        return dates_trips

    @property
    def mileage(self):
        distances = self.orders.filter(status=Order.STATUS_DONE).values_list('total_distance', flat=True)
        return sum(distances)

    @property
    def dimensions(self):
        return sorted([self.width_trunk, self.length_trunk, self.height_trunk])


class Repair(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, limit_choices_to=Q(is_repair=True), related_name='repairs'
    )
    what_repair = models.CharField(max_length=200)
    deadline = models.DateTimeField(default=timezone.now())
    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In UAH')


class Order(models.Model):
    STATUS_NEW = 1
    STATUS_PREPARE_TO_SHIP = 2
    STATUS_DONE = 3

    STATUS_CHOICES = (
        (STATUS_NEW, 'NEW'),
        (STATUS_PREPARE_TO_SHIP, 'PREPARE TO SHIP'),
        (STATUS_DONE, 'DONE')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)
    product = models.CharField(max_length=255)
    manager = models.ForeignKey(
        Manager, on_delete=models.PROTECT,
        related_name='orders', null=True
    )
    car = models.ForeignKey(
        Car, on_delete=models.PROTECT, limit_choices_to=Q(is_repair=False),
        related_name='orders', null=True
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.PROTECT,
        related_name='orders', null=True
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, default='+380')
    address = models.CharField(max_length=255)
    date_trip = models.DateTimeField(default=timezone.now())
    total_distance = models.DecimalField(max_digits=12, decimal_places=2, help_text='In kilometers', null=True)


class Fueling(TimeStampedModel):
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, related_name='fueling', null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, related_name='fueling', null=True)
    type_fuel = models.CharField(max_length=20, choices=Car.TYPE_OF_FUEL_CHOICES)
    amount_fuel = models.PositiveSmallIntegerField(help_text='In liters')
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In UAH'
    )
    fuel_check = models.ImageField(upload_to='checks/')
