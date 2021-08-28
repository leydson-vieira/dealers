from rest_framework import serializers

from .models import Dealer


class DealerCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    cpf = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Dealer
        fields = ('full_name', 'cpf', 'email', 'password')
