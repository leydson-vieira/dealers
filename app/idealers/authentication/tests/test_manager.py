import pytest

from ..models import Dealer


@pytest.mark.django_db
class TestDealerManager:
    def test_should_raise_validation_error_when_has_no_email(self):
        with pytest.raises(ValueError):
            Dealer.objects.create_user(
                full_name='Name',
                email='',
                password='blablabla',
                cpf='123456789',
            )

    def test_should_raise_validation_error_when_has_no_cpf(self):
        with pytest.raises(ValueError):
            Dealer.objects.create_user(
                full_name='Name',
                email='teste@teste.com',
                password='blablabla',
                cpf='',
            )

    def test_should_raise_validation_error_when_has_no_password(self):
        with pytest.raises(ValueError):
            Dealer.objects.create_user(
                full_name='Name',
                email='teste@teste.com',
                password='',
                cpf='123456789',
            )
