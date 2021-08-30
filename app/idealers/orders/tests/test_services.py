from decimal import Decimal
from datetime import datetime
from _pytest.config import exceptions
import pytest

from ..services import OrderService
from ..exceptions import DealerDoesNotExist
from ..models import Order


@pytest.mark.django_db
class TestOrderService:
    @pytest.fixture
    def order_data(self):
        return {
            'code': 'order_code',
            'amount': 5000,
            'date': datetime.now(),
            'cpf': '38723274884'
        }

    def test_should_not_create_an_order_because_delaer_doesnt_exist(self, user, order_data):
        order_data['cpf'] = '99999999999'
        with pytest.raises(DealerDoesNotExist):
            OrderService.create_order(**order_data)

    def test_should_create_an_order(self, order_data, user):
        order = OrderService.create_order(**order_data)
        assert order

    def test_order_should_generate_a_cashback(self, order_data, user):
        order = OrderService.create_order(**order_data)
        assert hasattr(order, 'cashback')

    @pytest.mark.parametrize(
        'order_amount,expected_cashback_amount',
        [
            (Decimal('100'), Decimal('10')),
            (Decimal('1000'), Decimal('100')),
            (Decimal('1500'), Decimal('225')),
            (Decimal('2000'), Decimal('400')),
        ]
    )
    def test_cashback_calcs(
        self, order_amount, expected_cashback_amount, order_data, settings, user
    ):
        settings.FIRST_LEVEL_CASHBACK_TARGET = 1000
        settings.FIRST_LEVEL_CASHBACK_PERCENT = '0.1'
        settings.SECOND_LEVEL_CASHBACK_TARGET = 1500
        settings.SECOND_LEVEL_CASHBACK_PERCENT = '0.15'
        settings.THIRD_LEVEL_CASHBACK_PERCENT = '0.20'

        order_data['amount'] = order_amount

        order = OrderService.create_order(**order_data)

        assert order.cashback.amount == expected_cashback_amount


    @pytest.mark.parametrize(
        "cpf,status",
        [
            ("38723274884", Order.Status.IN_VALIDATION),
            ("15350946056", Order.Status.APPROVED),
        ],
    )
    def test_should_return_status_validation_to_approved_cpf(
        self, cpf, status, order_data, user, approved_user
    ):
        order_data['cpf'] = cpf

        order = OrderService.create_order(**order_data)

        assert order.status == status
