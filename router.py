from typing import Annotated
from fastapi import APIRouter, Depends
from services import search_data
from serializers import (Payload,
                         IsinExistsFilterSerializer,
                         IsinExistsIntervalFilterSerializer,
                         IidToIsinFilterSerializer,
                         )

router = APIRouter(
    prefix="/api"
)


@router.get("/isin_exists")
async def isin_exists(
        attr: Annotated[IsinExistsFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)


@router.get("/isin_exists_interval")
async def isin_exists_interval(
        attr: Annotated[IsinExistsIntervalFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)


@router.get("/iid_to_isin")
async def iid_to_isin(
        attr: Annotated[IidToIsinFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)
