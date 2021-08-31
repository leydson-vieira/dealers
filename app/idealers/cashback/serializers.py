from rest_framework import serializers


class AccumulatedCashbackSerializer(serializers.Serializer):
    credit = serializers.IntegerField()
