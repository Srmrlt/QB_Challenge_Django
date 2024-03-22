from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.queries import OrmMethods
from services.xml_parser import parse_data
from router.router_api import router_api
from router.router_stream import router_stream


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
app.include_router(router_api)
app.include_router(router_stream)
