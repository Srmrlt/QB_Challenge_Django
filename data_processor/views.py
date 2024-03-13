from rest_framework.views import APIView
from rest_framework.response import Response

from data_processor.serializers import Payload
from data_processor.models import Instrument


class IsinExistsView(APIView):
    serializer_class = Payload

    def get(self, request):
        date = request.query_params.get('date')
        instrument = request.query_params.get('instrument')
        exchange = request.query_params.get('exchange')
        queryset = Instrument.objects.all()

        if date:
            queryset = queryset.filter(exchange__date__date=date)
        if instrument:
            queryset = queryset.filter(name=instrument)
        if exchange:
            queryset = queryset.filter(exchange__name=exchange)

        serializer = Payload(queryset, many=True)
        return Response({'result': serializer.data})


class IsinExistsIntervalView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        instrument = request.query_params.get('instrument')
        exchange = request.query_params.get('exchange')
        queryset = Instrument.objects.filter(
            exchange__date__date=date,
            name=instrument,
            exchange__name=exchange
        ).first()

        serializer = Payload(queryset)
        return Response({'result': serializer.data if queryset else None})


class IidToIsinView(APIView):
    def get(self, request):
        date = request.query_params.get('date')
        iid = int(request.query_params.get('iid'))
        queryset = Instrument.objects.filter(
            iid=iid,
            exchange__date__date=date
        ).first()

        serializer = Payload(queryset)
        return Response({'result': serializer.data if queryset else None})
