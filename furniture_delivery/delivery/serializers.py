from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.validators import UniqueForDateValidator

from delivery.models import Order, Fueling, Car, Repair, Driver, Manager
from rest_framework import serializers


class RepairListSerializer(serializers.ModelSerializer):
    """ Список ремонтів """
    class Meta:
        model = Repair
        fields = ('id', 'car', 'what_repair', 'deadline', 'cost')
        read_only_fields = ('car', 'what_repair', 'deadline', 'cost')


class AddRepairSerializer(serializers.ModelSerializer):
    """ Список ремонтів """

    def validate(self, data):
        if data['deadline'] < timezone.now():
            raise serializers.ValidationError(_("Unable to repair in the past"))
        return data

    class Meta:
        model = Repair
        fields = '__all__'


class AddFuelingSerializer(serializers.ModelSerializer):
    """ For register refueling """
    def validate(self, data):
        # check type fuel
        if data['type_fuel'] != data['car'].type_fuel:
            raise serializers.ValidationError(_('Wrong fuel type'))
        # check amount fuel to tank size
        elif data['amount_fuel'] > data['car'].tank_size:
            raise serializers.ValidationError(_(f"The tank holds the maximum {data['car'].tank_size}"))
        return data

    class Meta:
        model = Fueling
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class ShortCarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'title', 'state_number')


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('id', 'user',)


class DriverSerializer(serializers.ModelSerializer):
    mileage = serializers.CharField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ('id', 'user', 'mileage')


class StaffOrderSerializer(serializers.ModelSerializer):
    """ CRUD order for staff """
    validators = [
        UniqueForDateValidator(
            queryset=Order.objects.all(),
            field='car',
            date_field='date_trip'
        ),
        UniqueForDateValidator(
            queryset=Order.objects.all(),
            field='driver',
            date_field='date_trip'
        )
    ]

    def validate(self, data):
        if str(data['car'].driver_class) not in data['driver'].driver_class:
            raise serializers.ValidationError(_("This driver can't drive this car"))
        elif data['date_trip'] < timezone.now():
            raise serializers.ValidationError(_("Unable to order in the past"))
        return data

    class Meta:
        model = Order
        fields = '__all__'


class FutureOrderListSerializer(serializers.ModelSerializer):
    """ List order for staff """
    manager = ManagerSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    car = ShortCarListSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class ManagerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = '__all__'


class DriverListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    mileage = serializers.IntegerField(read_only=True)

    class Meta:
        model = Driver
        fields = ('id', 'user', 'mileage')


class FuelingSerializer(serializers.ModelSerializer):
    car = ShortCarListSerializer()

    class Meta:
        model = Fueling
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    """ Add order for customer """
    def validate(self, data):
        if data['date_trip'] < timezone.now():
            raise serializers.ValidationError(_("Unable to order in the past"))
        return data

    class Meta:
        model = Order
        exclude = ('id', 'status', 'manager', 'car', 'driver', 'total_distance')


class CarSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'title', 'load_capacity', 'width_trunk', 'length_trunk', 'height_trunk')
