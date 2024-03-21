from typing import Any
from database.queries import OrmMethods
from database.models import DateOrm, ExchangeOrm, InstrumentOrm


async def search_data(validated_data: dict[str, Any]):
    criteria = {
        DateOrm.date: validated_data.get('date'),
        InstrumentOrm.name: validated_data.get('instrument'),
        ExchangeOrm.name: validated_data.get('exchange'),
        InstrumentOrm.iid: validated_data.get('iid'),
    }
    conditions = [field == value for field, value in criteria.items() if value is not None]

    if validated_data.get('date_from'):
        conditions.append(DateOrm.date >= validated_data.get('date_from'))
    if validated_data.get('date_to'):
        conditions.append(DateOrm.date <= validated_data.get('date_to'))
    data = await OrmMethods.find_data(conditions)

    return data
