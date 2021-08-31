from datetime import datetime
from decimal import Decimal
from typing import Optional

from django.conf import settings

from authentication.models import Dealer
from cashback.models import Cashback

from .exceptions import (DealerDoesNotExist, OrderCodeAlreadyExists,
                         OrderDoesNotExist, StatusNotAllowed)
from .models import Order


class OrderService:
    @classmethod
    def create_order(
        cls: 'OrderService',
        code: str,
        amount: Decimal,
        date: datetime,
        cpf: str,
    ) -> Order:
        dealer: Dealer = cls.get_dealer_or_raise_exception(code=code, cpf=cpf)

        status = Order.Status.IN_VALIDATION
        if cpf in settings.APPROVED_ALLOWED_DEALERS:
            status = Order.Status.APPROVED

        order = Order.objects.create(
            code=code, amount=amount, date=date, dealer=dealer, status=status
        )

        cls._create_or_update_cashback_by_order(order)

        return order

    @classmethod
    def update_order(cls: 'OrderService', order_id: str, **kwargs) -> Order:
        cpf: str = kwargs.get('cpf')
        code: str = kwargs.get('code')

        if cpf or code:
            dealer: Dealer = cls.get_dealer_or_raise_exception(code=code, cpf=cpf)

        order = Order.objects.filter(pk=order_id).first()
        if not order:
            raise OrderDoesNotExist()
        if order.status != Order.Status.IN_VALIDATION:
            raise StatusNotAllowed()

        for attr, value in kwargs.items():
            setattr(order, attr, value)

        order.save()
        
        cls._create_or_update_cashback_by_order(order)

        return order

    @staticmethod
    def list_orders():
        return list(Order.objects.all()[:20])

    @staticmethod
    def delete_order(order_id: str) -> None:
        order: Order = Order.objects.filter(pk=order_id).first()

        if not order:
            raise OrderDoesNotExist()
        if order.status != Order.Status.IN_VALIDATION:
            raise StatusNotAllowed()

        order.delete()

    @staticmethod
    def get_dealer_or_raise_exception(cpf: str, code: Optional[str] = None) -> None:
        if code:
            if Order.objects.filter(code=code).exists():
                raise OrderCodeAlreadyExists()
        
        dealer: Dealer = Dealer.objects.filter(cpf=cpf).first()
        if not dealer:
            raise DealerDoesNotExist()

        return dealer

    @staticmethod
    def _create_or_update_cashback_by_order(order: Order) -> None:
        """
        Creates cashback based on order instance and apply the level rules
        """
        first_level_cashback_percent = Decimal(settings.FIRST_LEVEL_CASHBACK_PERCENT)
        second_level_cashback_percent = Decimal(settings.SECOND_LEVEL_CASHBACK_PERCENT)
        third_level_cashback_percent = Decimal(settings.THIRD_LEVEL_CASHBACK_PERCENT)

        if order.amount <= settings.FIRST_LEVEL_CASHBACK_TARGET:
            amount = order.amount * first_level_cashback_percent
            percentage = first_level_cashback_percent
    
        elif order.amount <= settings.SECOND_LEVEL_CASHBACK_TARGET:
            amount = order.amount * second_level_cashback_percent
            percentage = second_level_cashback_percent

        else:
            amount = order.amount * third_level_cashback_percent
            percentage = third_level_cashback_percent
        
        cashback: Cashback = Cashback.objects.filter(order=order).first()
        if cashback:
            cashback.amount = amount
            cashback.percentage = percentage
            cashback.save()
        else:
            Cashback.objects.create(order=order, amount=amount, percentage=percentage)
