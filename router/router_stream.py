from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse
from services.file_streaming import configure_stream_response
from serializers import StreamSerializer


router_stream = APIRouter(tags=['Stream'])


@router_stream.get("/stream")
async def stream_binary_file(
        attr: Annotated[StreamSerializer, Depends()]
):
    s_attr = attr.model_dump()
    return StreamingResponse(**await configure_stream_response(s_attr))
