import pytest

from rest_framework import status

from django.urls import reverse

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
