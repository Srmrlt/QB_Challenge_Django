from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.queries import OrmMethods
from xml_parser import parse_data
from router import router_search, router_stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    await OrmMethods.delete_tables()
    await OrmMethods.create_tables()
    print("The database is cleaned and ready to go")
    await parse_data()
    print("Date parsed successfully")
    yield
    print("Shutdown")


app = FastAPI(lifespan=lifespan)
app.include_router(router_search)
app.include_router(router_stream)
