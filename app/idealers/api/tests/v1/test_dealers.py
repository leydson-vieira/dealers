import pytest
from django.urls import reverse
from rest_framework import status

from authentication.models import Dealer


@pytest.mark.django_db
class TestApiV1Dealers:
    @pytest.fixture
    def payload(self):
        return {
            'full_name': 'First Test User',
            'cpf': '387.232.748-85',
            'email': 'teste@teste.com',
            'password': 'teste123'
        }

    def test_should_create_dealer(self, unlogged_client, payload):
        # disable credentials
        unlogged_client.credentials()
        response = unlogged_client.post(reverse('dealers'), payload)

        assert response.status_code == status.HTTP_201_CREATED

    def test_should_not_create_dealer_with_existing_mail(
        self, unlogged_client, payload
    ):
        # email that already exists
        payload['email'] = 'leydson.vieira@gmail.com'

        response = unlogged_client.post(reverse('dealers'), payload)

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_should_not_create_dealer_with_existing_cpf(
        self, unlogged_client, payload
    ):
        # cpf that already exists
        payload['cpf'] = '38723274884'

        response = unlogged_client.post(reverse('dealers'), payload)

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_should_create_dealer_cpf_without_punctuation(
        self, logged_client, payload
    ):
        response = logged_client.post(reverse('dealers'), payload)
        dealer = Dealer.objects.get(email='teste@teste.com')

        assert response.status_code == status.HTTP_201_CREATED
        assert dealer.cpf == '38723274885'
