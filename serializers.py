import datetime
from pydantic import BaseModel


class Payload(BaseModel):
    instrument: str
    exchange: str
    iid: int
    storage_type: int
    

class IsinExistsFilterSerializer(BaseModel):
    date: datetime.date
    instrument: str
    exchange: str


class IsinExistsIntervalFilterSerializer(BaseModel):
    date_from: datetime.date
    date_to: datetime.date
    instrument: str
    exchange: str


class IidToIsinFilterSerializer(BaseModel):
    date: datetime.date
    iid: int
