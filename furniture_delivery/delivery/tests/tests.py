import pytest
import json

from datetime import timedelta
from collections import OrderedDict
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


def test_path_order_unique_date_car_error(api_client, order_date_check, car, driver, manager):
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
        "date_trip": "2022-05-31T19:10:00+03:00"
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "car": [
            'This field must be unique for the "date_trip" date.'
        ]
    }


def test_path_order_unique_date_driver_error(api_client, order_date_check, car2, driver, manager):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    order = baker.make(
        Order, manager=manager, car=car2, driver=driver, status=Order.STATUS_PREPARE_TO_SHIP,
        product="Table", name="Petro", phone="777", address="Dim", total_distance=None
    )

    resp = api_client.patch(f'/api/v1/staff-order/{order.id}/', {
        "product": "Table",
        "car": car2.id,
        "driver": driver.id,
        "manager": manager.id,
        "date_trip": "2022-05-31T19:10:00+03:00"
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "driver": [
            "This field must be unique for the \"date_trip\" date."
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
        "amount_fuel": car.tank_size + 1,
        "price": 2500,
        "car": car.id,
        "driver": driver.id
    })

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.data == {
        "non_field_errors": [
            f"The tank holds the maximum {car.tank_size}"
        ]
    }


def test_view_cars(api_client, car, car2, car3):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.get(
        '/api/v1/cars/?product_weight=400&product_width=3&product_length=2&product_height=1',
        content_type='application/json'
    )

    assert resp.status_code == status.HTTP_200_OK
    data = json.loads(json.dumps(resp.data))

    for item in data:
        assert 'id' in item
        del item['id']
        assert 'dates_future_orders' in item
        del item['dates_future_orders']
    print(data)
    assert data == [
        {
            "driver_class": 2,
            "height_trunk": "2.00",
            "length_trunk": "5.00",
            "load_capacity": "500.00",
            "title": "Renault",
            "width_trunk": "2.00",
        },
        {
            "driver_class": 3,
            "height_trunk": "3.00",
            "length_trunk": "15.00",
            "load_capacity": "800.00",
            "title": "Jeep",
            "width_trunk": "3.00",
        },
    ]


def test_view_null_cars(api_client, car, car2, car3):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.get(
        '/api/v1/cars/?product_weight=4000&product_width=3&product_length=20&product_height=1',
        content_type='application/json'
    )

    assert resp.status_code == status.HTTP_200_OK
    data = json.loads(json.dumps(resp.data))

    for item in data:
        assert 'id' in item
        del item['id']
        assert 'dates_future_orders' in item
        del item['dates_future_orders']
    print(data)
    assert data == []


def test_add_repair(api_client, car4, driver4):
    user = User.objects.get(username='admin')
    api_client.force_login(user)

    deadline = timezone.now() + timedelta(days=1)

    resp = api_client.post('/api/v1/add-repair/', {
        "what_repair": "Engine",
        "deadline": deadline,
        "cost": 5000,
        "car": car4.id
    })
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.data

    assert 'id' in data
    del data['id']
    assert 'deadline' in data
    del data['deadline']

    assert data == {
        "what_repair": "Engine",
        "cost": "5000.00",
        "car": car4.id
    }

