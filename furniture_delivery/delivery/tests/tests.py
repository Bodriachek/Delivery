from datetime import timedelta

import pytest

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status

from delivery.models import Car

pytestmark = pytest.mark.django_db


# def test_add_order(api_client, car, driver):
#     resp = api_client.post('/api/v1/add-order/', {
#         "product": "Chair",
#         "name": "Petro",
#         "phone": "777",
#         "address": "Dim",
#         "date_trip": timezone.now() + timedelta(days=1)
#     })
#     print(resp.data)
#     assert resp.status_code == status.HTTP_201_CREATED
#     data = resp.data
#
#     assert 'id' in data
#     order_id = data['id']
#     del data['id']
#
#     assert 'date_trip' in data
#     del data['date_trip']
#
#     assert data == {
#         "product": "Chair",
#         "name": "Petro",
#         "phone": "777",
#         "address": "Dim",
#     }
#
#     user = User.objects.get(username='admin')
#     api_client.force_login(user)
#
#     resp = api_client.patch(
#         f'/api/v1/staff-order/{order_id}/', dict(
#             product="Table", car=car, driver=driver, date_trip=timezone.now() + timedelta(days=1))
#     )
#     print(resp.data)
#     assert resp.status_code == status.HTTP_200_OK
#     data = resp.data
#
#     assert 'id' in data
#     del data['id']
#
#     assert data == {
#         "product": "Table",
#         "name": "Petro",
#         "phone": "777",
#         "address": "Dim",
#         "date_trip": None
#     }

#
# def test_add_fueling(api_client, car, driver):
#     user = User.objects.get(username='admin')
#     api_client.force_login(user)
#
#     resp = api_client.post('/api/v1/add-fueling/', {
#         "type_fuel": Car.GAS,
#         "amount_fuel": 50,
#         "price": 2500,
#     })
#     print(resp.data)
#     assert resp.status_code == status.HTTP_201_CREATED
#     data = resp.data
#
#     assert 'id' in data
#     fueling_id = data['id']
#     del data['id']
#
#     assert data == {
#         "type_fuel": car.GAS,
#         "amount_fuel": "50",
#         "price": "2500",
#     }
#
#     resp = api_client.get(f'/api/v1/fueling-list/{fueling_id}/')
#     assert resp.status_code == status.HTTP_200_OK
#     data = resp.data
#
#     assert 'id' in data
#     del data['id']
#
#     assert data == {
#         "type_fuel": car.GAS,
#         "amount_fuel": "50",
#         "price": "2500",
#         "fuel_check": None
#     }


