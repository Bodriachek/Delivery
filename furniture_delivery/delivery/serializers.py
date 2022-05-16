from django import views
from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework.templatetags.rest_framework import data

from delivery.models import Order, Fueling, Car, Repair, Driver
from rest_framework import serializers


class CreateOrderSerializer(serializers.ModelSerializer):
    """ Add order for customer """
    class Meta:
        model = Order
        exclude = ('id', 'status', 'manager', 'car', 'driver', 'total_distance')


class ChangeOrderSerializer(serializers.ModelSerializer):
    """ Change and list order for staff """

    class Meta:
        model = Order
        fields = '__all__'


class ManagerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('manager',)


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


class CarListSerializer(serializers.ModelSerializer):
    mileage = serializers.CharField(read_only=True)

    class Meta:
        model = Car
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Driver
        fields = '__all__'


class DriverListSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    car = CarListSerializer()

    class Meta:
        model = Order
        fields = ('id', 'driver', 'car')

    def get_driver(self, obj):
        return UserSerializer(obj.driver.user).data


class FuelingSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    car = CarListSerializer()

    class Meta:
        model = Fueling
        fields = '__all__'

    def get_driver(self, obj):
        return UserSerializer(obj.driver.user).data
