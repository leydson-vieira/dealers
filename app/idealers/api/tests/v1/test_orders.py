from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from cashback.models import Cashback
from orders.models import Order


@pytest.mark.django_db
class TestApiV1Orders:
    @pytest.fixture
    def order(self, user):
        return Order.objects.create(
            code='007162t35',
            dealer=user,
            amount='5500',
            date='2021-08-28T13:45:00.000Z',
        )

    @pytest.fixture
    def cashback(self, order):
        return Cashback.objects.create(
            order=order,
            amount=Decimal('100'),
            percentage=Decimal('.1'),
        )

    @pytest.fixture
    def payload(self):
        return {
            "code": "007162t35",
            "cpf": "38723274884",
            "amount": "5200.50",
            "date": "2021-08-28T13:45:00.000Z"
        }

    def test_should_return_unauthorized(self, unlogged_client, payload):
        # disable credentials
        unlogged_client.credentials()
        response = unlogged_client.post(reverse('orders'), payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_should_not_create_with_cpf_doesnt_exist(self, logged_client, payload):
        payload['cpf'] = '99999999999'
        response = logged_client.post(reverse('orders'), payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_not_create_with_existing_code(self, logged_client, payload, order):
        response = logged_client.post(reverse('orders'), payload)

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_should_create_an_order(self, logged_client, payload):
        response = logged_client.post(reverse('orders'), payload)

        assert response.status_code == status.HTTP_201_CREATED

    def test_should_delete_an_order(self, logged_client, order):
        response = logged_client.delete(
            reverse('orders-detail', kwargs={'order_id': str(order.pk)})
        )

        assert response.status_code == status.HTTP_200_OK

    def test_should_not_delete_an_order_when_not_found(self, logged_client):
        response = logged_client.delete(
            reverse(
                'orders-detail',
                kwargs={'order_id': '2fa3a532-94ee-4e82-8372-57fc97644ab3'},
            )
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_not_delete_an_order_when_not_in_validation(
        self, logged_client, order
    ):
        order.status = Order.Status.APPROVED
        order.save()

        response = logged_client.delete(
            reverse('orders-detail', kwargs={'order_id': str(order.pk)})
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_list_orders(self, logged_client, cashback):

        response = logged_client.get(reverse('orders'))

        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data[0]['id'] == str(cashback.order.id)

    def test_should_update_an_order(self, logged_client, cashback):
        payload = {
            "amount": "150",
            "date": "2021-08-28T13:45:00.000Z"
        }

        response = logged_client.patch(
            reverse('orders-detail', kwargs={'order_id': str(cashback.order.id)}),
            payload,
        )

        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data['id'] == str(cashback.order.id)

    def test_should_not_update_an_order_when_code_already_exist(
        self, logged_client, cashback
    ):
        payload = {
            "code": "007162t35",
            "cpf": "38723274884",
            "amount": "5200.50",
            "date": "2021-08-28T13:45:00.000Z"
        }

        response = logged_client.patch(
            reverse('orders-detail', kwargs={'order_id': str(cashback.order.id)}),
            payload,
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_should_not_update_an_order_when_not_exist(self, logged_client):
        payload = {
            "amount": "5200.50",
            "date": "2021-08-28T13:45:00.000Z"
        }

        response = logged_client.patch(
            reverse(
                'orders-detail',
                kwargs={'order_id': '2fa3a532-94ee-4e82-8372-57fc97644ab3'},
            ),
            payload,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_not_update_an_order_when_not_in_validation(
        self, logged_client, cashback
    ):
        cashback.order.status = Order.Status.REJECTED
        cashback.order.save()

        payload = {
            "amount": "5200.50",
            "date": "2021-08-28T13:45:00.000Z"
        }

        response = logged_client.patch(
            reverse(
                'orders-detail', kwargs={'order_id': str(cashback.order.id)}
            ),
            payload,
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
