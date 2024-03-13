import os.path

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from data_processor.serializers import Payload
from data_processor.models import Instrument
from data_processor.utils import read_file_in_chunks


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


def stream_binary_file(request, file_path):
    """
    Streams a file in chunks to the client.

    :param request: HttpRequest object, used to access GET parameters.
    :param file_path: The relative path to the file to be streamed.
    :return: A StreamingHttpResponse if the file exists and is readable,
             HttpResponseBadRequest if 'chunk_size' parameter is invalid,
             or HttpResponseNotFound if the file does not exist.
    """
    chunk_size = request.GET.get('chunk_size', 1024*10)

    # Convert 'chunk_size' to integer, raise ValueError if conversion fails
    try:
        chunk_size = int(chunk_size)
    except ValueError:
        return HttpResponseBadRequest('Invalid chunk_size format')

    # Join the requested 'file_path' with the base 'data' directory
    file_path = os.path.join('data', file_path)

    # Check if the file exists; return a 404 Not Found response if it doesn't
    if not os.path.exists(file_path):
        return HttpResponseNotFound('File not found')

    try:
        response = StreamingHttpResponse(read_file_in_chunks(file_path, chunk_size),
                                         content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_path.split('/')[-1])
        return response
    except Exception as e:
        HttpResponseBadRequest(e)
