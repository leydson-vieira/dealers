import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from authentication.models import Dealer


@pytest.fixture
def user():
    return Dealer.objects.create_user(
        full_name='Leydson Vieira',
        cpf='38723274884',
        email='leydson.vieira@gmail.com',
        password='password'
    )

@pytest.fixture
def unlogged_client(user):
    client = APIClient()
    return client

@pytest.fixture
def logged_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client