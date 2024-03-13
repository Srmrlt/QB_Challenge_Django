from rest_framework import serializers

from data_processor.models import Instrument


class Payload(serializers.ModelSerializer):
    exchange = serializers.CharField(source='exchange.name')

    class Meta:
        model = Instrument
        fields = ['name', 'exchange', 'iid', 'storage_type']
