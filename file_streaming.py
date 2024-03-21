import os
import aiofiles
from typing import Any, AsyncGenerator
from fastapi import HTTPException


async def configure_stream_response(validated_data: dict[str, Any]) -> dict[str, Any]:
    """
    Prepares parameters for a StreamingResponse based on validated data.

    Args:
        validated_data (dict[str, Any]): Dictionary of validated data needed for setting up the response.

    Returns:
        dict[str, Any]: Dictionary with 'content' and 'headers' keys, ready to be used in a StreamingResponse.
    """
    chunk_size = validated_data.get('chunk')
    date = validated_data.get('date')
    filename = validated_data.get('filename')
    file_path = os.path.join('data', str(date.year), str(date.month), str(date.day), filename)
    await __check_file_availability(file_path)
    file_size = os.path.getsize(file_path)
    headers = {
        'Content-Length': str(file_size),
        'Content-Disposition': f'attachment; filename="{os.path.basename(file_path)}"',
    }
    content = __read_file_in_chunks(file_path, chunk_size)

    return {
        'content': content,
        'headers': headers,
    }


async def __check_file_availability(file_path: str):
    """
    Asynchronously checks if file exists, raises error if not.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")


async def __read_file_in_chunks(file_path: str, chunk_size: int) -> AsyncGenerator[bytes]:
    """
    Asynchronously read a file in chunks of a specified size.

    :param file_path: The path to the file to be read.
    :param chunk_size: The size of each chunk to read, in bytes.
    :return: An iterator over the chunks of the file.
    """
    try:
        async with aiofiles.open(file_path, 'rb') as file:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while reading the file: {e}")
