import pytest

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
def approved_user():
    return Dealer.objects.create_user(
        full_name='Revendedor Aprovado',
        cpf='15350946056',
        email='aprovadoa@gmail.com',
        password='password'
    )
