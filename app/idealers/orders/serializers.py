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
