import string

from rest_framework import serializers

from .models import Dealer


class CpfField(serializers.Field):
    """
    Field to save CPF without punctuation
    """
    def to_internal_value(self, value):
        return value.translate(str.maketrans('', '', string.punctuation))


class DealerCreateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    cpf = CpfField()
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = Dealer
        fields = ('full_name', 'cpf', 'email', 'password')
