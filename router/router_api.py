from typing import Annotated
from fastapi import APIRouter, Depends
from services.data_search import data_search
from schema import (Payload,
                    IsinExistsFilterSchema,
                    IsinExistsIntervalFilterSchema,
                    IidToIsinFilterSchema,
                    )

router_api = APIRouter(
    prefix="/api",
    tags=['API'],
)


@router_api.get("/isin_exists")
async def isin_exists(
        attr: Annotated[IsinExistsFilterSchema, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await data_search(s_attr)


@router_api.get("/isin_exists_interval")
async def isin_exists_interval(
        attr: Annotated[IsinExistsIntervalFilterSchema, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await data_search(s_attr)


@router_api.get("/iid_to_isin")
async def iid_to_isin(
        attr: Annotated[IidToIsinFilterSchema, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await data_search(s_attr)
