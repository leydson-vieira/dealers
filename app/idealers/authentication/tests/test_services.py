import pytest

from ..services import DealerService
from ..exceptions import DealerAlreadyExists

@pytest.mark.django_db
class TestDealerService:
    def test_should_raise_error_when_dealer_exist(self, user):
        with pytest.raises(DealerAlreadyExists):
            DealerService.create_dealer(
                full_name='Leydson Vieira',
                cpf='38723274884',
                email='leydson.vieira@gmail.com',
                password='password'
            )

    def test_should_create_user(self):
        user = DealerService.create_dealer(
            full_name='Leydson Vieira',
            cpf='38723274884',
            email='leydson.vieira@gmail.com',
            password='password'
        )
        
        assert user
