from datetime import datetime
from decimal import Decimal

from django.conf import settings

from authentication.models import Dealer
from cashback.models import Cashback

from .models import Order
from .exceptions import DealerDoesNotExist, OrderCodeAlreadyExists


class OrderService:
    @classmethod
    def create_order(
        cls: 'OrderService',
        code: str,
        amount: Decimal,
        date: datetime,
        cpf: str
    ) -> Order:
        if Order.objects.filter(code=code).exists():
            raise OrderCodeAlreadyExists()
        
        dealer: Dealer = Dealer.objects.filter(cpf=cpf).first()
        if not dealer:
            raise DealerDoesNotExist()

        order = Order.objects.create(code=code, amount=amount, date=date, dealer=dealer)
        cls._check_and_create_cashback_by_order(order)

        return order

    @staticmethod
    def _check_and_create_cashback_by_order(order: Order) -> None:
        first_level_cashback_percent = Decimal(settings.FIRST_LEVEL_CASHBACK_PERCENT)
        second_level_cashback_percent = Decimal(settings.SECOND_LEVEL_CASHBACK_PERCENT)
        third_level_cashback_percent = Decimal(settings.THIRD_LEVEL_CASHBACK_PERCENT)

        if order.amount < settings.FIRST_LEVEL_CASHBACK_TARGET:
            amount = order.amount * first_level_cashback_percent
            percentage = first_level_cashback_percent
    
        elif order.amount <= settings.SECOND_LEVEL_CASHBACK_TARGET:
            amount = order.amount * second_level_cashback_percent
            percentage = second_level_cashback_percent

        else:
            amount = order.amount * third_level_cashback_percent
            percentage = third_level_cashback_percent

        Cashback.objects.create(order=order, amount=amount, percentage=percentage)
