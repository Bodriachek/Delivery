from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.utils import timezone
from model_utils.models import TimeStampedModel
from multiselectfield import MultiSelectField


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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

    def __str__(self):
        return self.user.first_name


class Car(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    state_number = models.CharField(max_length=10, null=True)
    driver_class = models.PositiveIntegerField(choices=Driver.DRIVER_CLASS_CHOICES, default=Driver.DRIVER_CLASS_B)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    load_capacity = models.FloatField(help_text='In kilograms')
    width_trunk = models.FloatField(help_text='In meters')
    length_trunk = models.FloatField(help_text='In meters')
    height_trunk = models.FloatField(help_text='In meters')

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
    tank_size = models.FloatField(null=True, help_text='In liters')
    fuel_consumption = models.FloatField(null=True)

    # РЕМОНТ
    is_repair = models.BooleanField(default=False)

    @property
    def mileage(self):
        distances = self.orders.filter(status=Order.STATUS_DONE).values_list('total_distance', flat=True)
        return sum(distances)

    def __str__(self):
        return self.title


class Repair(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, limit_choices_to=Q(is_repair=True)
    )
    what_repair = models.CharField(max_length=200)
    deadline = models.DateField(default=timezone.now())
    cost = models.PositiveIntegerField(blank=True, null=True, help_text='In UAH')


class Order(models.Model):
    STATUS_NEW = 1
    STATUS_IN_PROCESSING = 2
    STATUS_PREPARE_TO_SHIP = 3
    STATUS_DONE = 4

    STATUS_CHOICES = (
        (STATUS_NEW, 'NEW'),
        (STATUS_IN_PROCESSING, 'IN PROCESSING'),
        (STATUS_PREPARE_TO_SHIP, 'PREPARE TO SHIP'),
        (STATUS_DONE, 'DONE')
    )

    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_NEW)
    product = models.CharField(max_length=255, null=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, limit_choices_to=Q(is_repair=False), blank=True, null=True,
        related_name='orders', unique_for_date='date_trip'
    )
    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, blank=True,
        related_name='orders', null=True, unique_for_date='date_trip'
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, default='+380')
    address = models.CharField(max_length=255, blank=True, null=True,)
    date_trip = models.DateField(default=timezone.now())
    total_distance = models.FloatField(default=0, help_text='In kilometers')


class Fueling(TimeStampedModel):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, related_name='car')
    type_fuel = models.CharField(max_length=20, choices=Car.TYPE_OF_FUEL_CHOICES, null=True)
    amount_fuel = models.FloatField(help_text='In liters', null=True)
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text='In UAH'
    )
    fuel_check = models.ImageField(upload_to='checks/', unique=True)

