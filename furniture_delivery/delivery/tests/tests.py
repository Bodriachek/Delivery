from datetime import timedelta

import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from model_bakery import baker
from rest_framework import status

from delivery.models import Car, Order, Fueling

pytestmark = pytest.mark.django_db


def test_add_order(api_client, car, driver, manager):
    date_trip = timezone.now() + timedelta(days=1)

    resp = api_client.post('/api/v1/add-order/', {
        "product": "Chair",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "date_trip": date_trip
    })
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.data

    assert 'id' in data
    order_id = data['id']
    del data['id']

    assert 'date_trip' in data
    del data['date_trip']

    assert data == {
        "product": "Chair",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
    }

    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.patch(
        f'/api/v1/staff-order/{order_id}/', dict(
            product="Table", car=car.id, driver=driver.id, date_trip=date_trip, manager=manager.id
        )
    )

    assert resp.status_code == status.HTTP_200_OK
    data = resp.data

    assert 'id' in data
    del data['id']
    assert 'date_trip' in data
    del data['date_trip']

    assert data == {
        "car": car.id,
        "manager": manager.id,
        "driver": driver.id,
        "status": Order.STATUS_NEW,
        "product": "Table",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "total_distance": None,
    }


def test_path_order_driver_class_error(api_client, car, driver2, manager):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    date_trip = timezone.now() + timedelta(days=1)

    order = baker.make(
        Order, manager=manager, car=car, driver=driver2, status=Order.STATUS_PREPARE_TO_SHIP,
        product="Table", name="Petro", phone="777", address="Dim", total_distance=None
    )

    resp = api_client.patch(f'/api/v1/staff-order/{order.id}/', {
        "product": "Table",
        "car": car.id,
        "driver": driver2.id,
        "manager": manager.id,
        "date_trip": date_trip
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "non_field_errors": [
            "This driver can't drive this car"
        ]
    }


def test_path_order_past_date_error(api_client, car, driver, manager):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    order = baker.make(
        Order, manager=manager, car=car, driver=driver, status=Order.STATUS_PREPARE_TO_SHIP,
        product="Table", name="Petro", phone="777", address="Dim", total_distance=None
    )

    resp = api_client.patch(f'/api/v1/staff-order/{order.id}/', {
        "product": "Table",
        "car": car.id,
        "driver": driver.id,
        "manager": manager.id,
        "date_trip": timezone.now() - timedelta(days=1)
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "non_field_errors": [
            "Unable to order in the past"
        ]
    }


def test_add_fueling(api_client, car, driver):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.post('/api/v1/add-fueling/', {
        "type_fuel": car.type_fuel,
        "amount_fuel": 50,
        "price": 2500,
        "car": car.id,
        "driver": driver.id
    })
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.data

    assert 'id' in data
    del data['id']
    assert 'created' in data
    del data['created']
    assert 'modified' in data
    del data['modified']

    assert data == {
        "type_fuel": car.type_fuel,
        "amount_fuel": 50,
        "price": "2500.00",
        "fuel_check": None,
        "car": car.id,
        "driver": driver.id
    }


def test_view_fueling(api_client, car, driver):
    fueling = baker.make(
        Fueling, type_fuel=car.type_fuel, amount_fuel=50, price=2500, car=car, driver=driver
    )

    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.get(f'/api/v1/fueling-list/{fueling.id}/')
    assert resp.status_code == status.HTTP_200_OK
    data = resp.data

    assert 'id' in data
    del data['id']
    assert 'created' in data
    del data['created']
    assert 'modified' in data
    del data['modified']

    assert data == {
        "type_fuel": car.type_fuel,
        "amount_fuel": 50,
        "price": "2500.00",
        "fuel_check": None,
        "driver": driver.id,
        "car": {
            "id": car.id,
            "title": car.title,
            "state_number": car.state_number
        },
    }


def test_add_fueling_type_fuel_error(api_client, car, driver):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    # car.type_fuel is GAS
    resp = api_client.post('/api/v1/add-fueling/', {
        "type_fuel": Car.DIESEL,
        "amount_fuel": 50,
        "price": 2500,
        "car": car.id,
        "driver": driver.id
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "non_field_errors": [
            "Wrong fuel type"
        ]
    }


def test_add_fueling_amount_fuel_error(api_client, car, driver):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.post('/api/v1/add-fueling/', {
        "type_fuel": car.type_fuel,
        "amount_fuel": 100,
        "price": 2500,
        "car": car.id,
        "driver": driver.id
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "non_field_errors": [
            "The tank holds the maximum 50"
        ]
    }

