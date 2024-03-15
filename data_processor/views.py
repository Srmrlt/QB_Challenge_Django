import os.path

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from data_processor.serializers import *
from data_processor.services import get_filtered_instruments
from data_processor.utils import read_file_in_chunks


class IsinExistsView(APIView):
    """
    Handles GET requests for searching financial instruments based on filters like date, name, and exchange.
    Validates query parameters using IsinExistsFilterSerializer and retrieves matching instruments from the database.
    Returns serialized instrument data or an empty list.
    """
    def get(self, request):
        serializer = IsinExistsFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = get_filtered_instruments(serializer.validated_data,
                                     {'date': 'exchange__date__date',
                                      'instrument': 'name',
                                      'exchange': 'exchange__name'})
        serializer = Payload(queryset, many=True)
        return Response({'result': serializer.data})


class IsinExistsIntervalView(APIView):
    """
    Handles GET requests for finding financial instruments within a date range and other filters.
    Validates request with IsinExistsIntervalFilterSerializer and fetches filtered instruments.
    Returns serialized instrument data or an empty list.
    """
    def get(self, request):
        serializer = IsinExistsIntervalFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = get_filtered_instruments(serializer.validated_data,
                                     {'instrument': 'name', 'exchange': 'exchange__name'})
        serializer = Payload(queryset, many=True)
        return Response({'result': serializer.data if queryset else None})


class IidToIsinView(APIView):
    """
    Retrieves financial instruments by internal ID (IID) and date using IidToIsinFilterSerializer.
    Returns serialized instrument data or an empty list.
    """
    def get(self, request):
        serializer = IidToIsinFilterSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        queryset = get_filtered_instruments(serializer.validated_data,
                                     {'date': 'exchange__date__date', 'iid': 'iid'})
        serializer = Payload(queryset, many=True)
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
