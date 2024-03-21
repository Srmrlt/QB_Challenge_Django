from typing import Annotated
from fastapi import APIRouter, Depends
from services import search_data
from starlette.responses import StreamingResponse
from file_streaming import configure_stream_response
from serializers import (Payload,
                         IsinExistsFilterSerializer,
                         IsinExistsIntervalFilterSerializer,
                         IidToIsinFilterSerializer,
                         StreamSerializer,
                         )

router_search = APIRouter(
    prefix="/api"
)


@router_search.get("/isin_exists")
async def isin_exists(
        attr: Annotated[IsinExistsFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)


@router_search.get("/isin_exists_interval")
async def isin_exists_interval(
        attr: Annotated[IsinExistsIntervalFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)


@router_search.get("/iid_to_isin")
async def iid_to_isin(
        attr: Annotated[IidToIsinFilterSerializer, Depends()]
) -> list[Payload]:
    s_attr = attr.model_dump()
    return await search_data(s_attr)


router_stream = APIRouter()


@router_stream.get("/stream")
async def stream_binary_file(
        attr: Annotated[StreamSerializer, Depends()]
):
    s_attr = attr.model_dump()
    return StreamingResponse(**await configure_stream_response(s_attr))
