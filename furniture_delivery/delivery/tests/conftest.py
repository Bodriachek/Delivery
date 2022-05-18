import pytest
from django.contrib.auth.models import User
from model_bakery import baker
from delivery.models import Driver, Car, Order
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return baker.make(User, first_name='First name', email='e@mail.com')


@pytest.fixture
def driver(user):
    return baker.make(Driver, user=user)


@pytest.fixture
def car(driver):
    return baker.make(Car, driver=driver, type_fuel=Car.GAS, load_capacity=500, width_trunk=3,
                      length_trunk=15, height_trunk=2)


@pytest.fixture
def order(driver, car):
    return baker.make(Order, driver=driver, car=car)


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        baker.make(
            User, is_superuser=True, username='top_management', email='topMan@example.com', name='Top Manager'
        )

