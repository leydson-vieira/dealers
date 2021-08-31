from decimal import Decimal

from rest_framework import serializers

from .models import Order


class OrderCreateSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
    cpf = serializers.CharField()

    class Meta:
        model = Order
        fields = ('code', 'amount', 'date', 'cpf')


class OrderUpdateSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    date = serializers.DateTimeField(required=False)
    cpf = serializers.CharField(required=False)
    status = serializers.ChoiceField(Order.Status, required=False)

    class Meta:
        model = Order
        fields = ('code', 'amount', 'date', 'cpf', 'status')


class OrderListSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
    cpf = serializers.CharField(source='dealer.cpf')
    status = serializers.ChoiceField(Order.Status)
    cashback_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='cashback.amount'
    )
    cashback_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id',
            'code',
            'amount',
            'date',
            'cpf',
            'cashback_amount',
            'cashback_percentage',
            'status',
        )

    def get_cashback_percentage(self, obj):
        human_percentage = obj.cashback.percentage * Decimal('100')
        return f'{human_percentage}%'
