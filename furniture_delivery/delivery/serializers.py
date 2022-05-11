from django import views
from delivery.models import Order, RegistrationRefueling, Car
from rest_framework import serializers


class DriverListSerializer(serializers.ModelSerializer):
    # driver = serializers.SlugRelatedField(slug_field='name', read_only=True)
    mileage = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ('driver', 'mileage')


class ManagerListSerializer(serializers.ModelSerializer):
    manager = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Order
        fields = ('manager',)


class CreateOrderSerializer(serializers.ModelSerializer):
    """ Для оформлення замовлення """
    class Meta:
        model = Order
        exclude = (
            'status', 'manager', 'car', 'driver', 'total_distance', 'amount_trip'
        )


class OrderListSerializer(serializers.ModelSerializer):
    """ Список замовлень """
    driver = serializers.SlugRelatedField(slug_field='name', read_only=True)
    manager = serializers.SlugRelatedField(slug_field='name', read_only=True)
    car = serializers.SlugRelatedField(slug_field='title', read_only=True)
    order_status = serializers.SlugRelatedField(slug_field='status', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class RegisterRefuelingSerializer(serializers.ModelSerializer):
    """ Для реєстрації заправок """
    driver = serializers.SlugRelatedField(slug_field='name', read_only=True)
    car = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = RegistrationRefueling
        fields = '__all__'


class RefuelingListSerializer(serializers.ModelSerializer):
    """ Список заправок """
    fuel = serializers.SlugRelatedField(slug_field='type_fuel', read_only=True)

    class Meta:
        model = RegistrationRefueling
        exclude = (
            'driver', 'car', 'fuel_check'
        )


class AddRepairSerializer(serializers.ModelSerializer):
    """ Список ремонтів """

    # driver = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Car
        fields = ('title', 'what_repair', 'deadline', 'cost')


class RepairsSerializer(serializers.ModelSerializer):
    """ Список ремонтів """
    driver = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Car
        fields = ('driver', 'title', 'what_repair', 'deadline', 'cost')


class CarListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('title', 'load_capacity')
