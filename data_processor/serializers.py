from rest_framework import serializers

from data_processor.models import Instrument


class Payload(serializers.ModelSerializer):
    exchange = serializers.CharField(source='exchange.name')

    class Meta:
        model = Instrument
        fields = ['name', 'exchange', 'iid', 'storage_type']


class IsinExistsFilterSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    instrument = serializers.CharField(max_length=100, required=False)
    exchange = serializers.CharField(max_length=100, required=False)


class IsinExistsIntervalFilterSerializer(serializers.Serializer):
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    instrument = serializers.CharField(max_length=100, required=False)
    exchange = serializers.CharField(max_length=100, required=False)


class IidToIsinFilterSerializer(serializers.Serializer):
    date = serializers.DateField(required=False)
    iid = serializers.IntegerField(required=False)
