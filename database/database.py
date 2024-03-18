from typing import Annotated
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from database.config import settings


engine = create_async_engine(
    url=settings.db_url_asyncpg,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
