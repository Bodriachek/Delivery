from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from delivery.models import Order, Fueling, Car, Repair, Driver, Manager
from rest_framework import serializers


class RepairListSerializer(serializers.ModelSerializer):
    """ Список ремонтів """
    class Meta:
        model = Repair
        fields = ('car', 'what_repair', 'deadline', 'cost')
        read_only_fields = ('car', 'what_repair', 'deadline', 'cost')


class AddRepairSerializer(serializers.ModelSerializer):
    """ Список ремонтів """
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
        fields = ('first_name', 'last_name', 'email')


class AddDriverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver
        fields = '__all__'


class ShortCarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('title', 'state_number', 'width_trunk', 'length_trunk', 'height_trunk')


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Manager
        fields = ('user',)


class DriverSerializer(serializers.ModelSerializer):
    mileage = serializers.CharField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = ('user', 'mileage')


class StaffOrderSerializer(serializers.ModelSerializer):
    """ Create and update order for staff """
    def validate(self, data):
        # check type fuel
        if str(data['car'].driver_class) not in data['driver'].driver_class:
            raise serializers.ValidationError(_("This driver can't drive this car"))
        return data

    class Meta:
        model = Order
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
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
    mileage = serializers.CharField(read_only=True)

    class Meta:
        model = Driver
        fields = ('user', 'mileage')


class FuelingSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    car = ShortCarListSerializer()

    class Meta:
        model = Fueling
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    """ Add order for customer """

    class Meta:
        model = Order
        exclude = ('id', 'status', 'manager', 'car', 'driver', 'total_distance')


class CarSizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('width_trunk', 'length_trunk', 'height_trunk')

