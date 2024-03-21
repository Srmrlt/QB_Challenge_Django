import datetime
from typing import Optional
from pydantic import BaseModel, conint


class Payload(BaseModel):
    instrument: str
    exchange: str
    iid: int
    storage_type: str
    

class IsinExistsFilterSerializer(BaseModel):
    date: Optional[datetime.date] = None
    instrument: Optional[str] = None
    exchange: Optional[str] = None


class IsinExistsIntervalFilterSerializer(BaseModel):
    date_from: Optional[datetime.date] = None
    date_to: Optional[datetime.date] = None
    instrument: Optional[str] = None
    exchange: Optional[str] = None


class IidToIsinFilterSerializer(BaseModel):
    date: Optional[datetime.date] = None
    iid: Optional[int] = None


class StreamSerializer(BaseModel):
    date: datetime.date
    filename: str
    chunk: conint(gt=4*1024, le=512*1024) = 32*1024
