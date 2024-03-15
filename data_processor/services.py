from data_processor.models import Instrument


def get_filtered_instruments(validated_data, query2model_mapping: dict[str, str]):
    """
    Filters Instrument objects using criteria from validated_data.
    Handles standard and date range filters specified in query2model_mapping.

    Parameters:
    - validated_data (dict): Validated request data.
    - query2model_mapping (dict): Maps query params to Instrument model fields.

    Returns:
    - A QuerySet of filtered Instrument objects.
    """
    filter_args = {
        query2model_mapping[key]: value
        for key, value in validated_data.items()
        if key in query2model_mapping
    }

    date_from = validated_data.get('date_from', None)
    date_to = validated_data.get('date_to', None)
    if date_from and date_to:
        filter_args['exchange__date__date__range'] = (date_from, date_to)
    elif date_from:
        filter_args['exchange__date__date__gte'] = date_from
    elif date_to:
        filter_args['exchange__date__date__lte'] = date_to
    return Instrument.objects.filter(**filter_args)
