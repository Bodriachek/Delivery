# RetirementAccount
from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status


def test_add_order(api_client):
    # api_client.force_login()
    resp = api_client.get('/api/v1/order/')
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data == []

    resp = api_client.post('/api/v1/order/add/',
    {
        "product": "Chair",
        "name": "Petro",
        "phone": "777",
        "address": "Dim",
        "date_trip": None
    }
    )
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

    resp = api_client.patch(
        f'/api/v1/order/{order_id}/', dict(product="Table")
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
