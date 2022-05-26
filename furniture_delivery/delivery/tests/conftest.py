import pytest

from django.contrib.auth.models import User
from delivery.models import Driver, Car, Order, Manager
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        baker.make(
            User, is_superuser=True, is_staff=True, username='admin', email='admin@example.com', first_name='Main admin'
        )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return baker.make(User, first_name='First name', email='e@mail.com')


@pytest.fixture
def driver(user):
    return baker.make(Driver, user=user, driver_class=["1", "2", "3"],)


@pytest.fixture
def user_driver2():
    return baker.make(User, first_name='First name', email='e@mail.com')


@pytest.fixture
def driver2(user_driver2):
    return baker.make(Driver, user=user_driver2, driver_class=["1", "2"],)


@pytest.fixture
def car(driver):
    return baker.make(
        Car, title='Jeep', driver=driver, type_fuel=Car.GAS, tank_size=50,
        driver_class=3,
        load_capacity=800, width_trunk=3, length_trunk=15, height_trunk=3
    )


@pytest.fixture
def car2(driver2):
    return baker.make(
        Car, title='Mercedes-benz', driver=driver2, type_fuel=Car.DIESEL, tank_size=50,
        driver_class=1,
        load_capacity=300, width_trunk=1, length_trunk=2, height_trunk=1
    )


@pytest.fixture
def order(driver, car):
    return baker.make(Order, driver=driver, car=car)


@pytest.fixture
def order_date_check(driver, car):
    return baker.make(Order, driver=driver, car=car, date_trip="2022-05-31T19:10:00+03:00")


@pytest.fixture
def user_manager():
    return baker.make(User, first_name='Name', email='manager@gmail.com', is_staff=True)


@pytest.fixture
def manager(user_manager):
    return baker.make(Manager, user=user_manager)

