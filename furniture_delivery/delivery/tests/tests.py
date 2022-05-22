import pytest

from django.contrib.auth.models import User
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_add_order(api_client):
    resp = api_client.post('/api/v1/order-add/', {
        "product": "Chair",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "date_trip": "2022-12-20"
    })
    print(resp.data)
    assert resp.status_code == status.HTTP_201_CREATED
    data = resp.data

    assert 'id' in data
    order_id = data['id']
    del data['id']

    assert data == {
        "product": "Chair",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "date_trip": None
    }

    user = User.objects.get(username='admin')
    api_client.force_login(user)

    resp = api_client.patch(
        f'/api/v1/orders/{order_id}/', dict(product="Table")
    )
    assert resp.status_code == status.HTTP_200_OK
    data = resp.data

    assert 'id' in data
    del data['id']

    assert data == {
        "product": "Table",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "date_trip": None
    }
