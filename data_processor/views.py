import os.path

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import StreamingHttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from data_processor.serializers import *
from data_processor.services import *
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
    try:
        chunk_size = check_chunk_size(request)
        full_file_path = check_file_availability(file_path)

        response = StreamingHttpResponse(read_file_in_chunks(full_file_path, chunk_size),
                                         content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(full_file_path)}"'
        return response
    except ValueError as e:
        return HttpResponseBadRequest(e)
    except FileNotFoundError:
        return HttpResponseNotFound('File not found')
    except Exception as e:
        return HttpResponseBadRequest(f'Error reading file: {e}')
