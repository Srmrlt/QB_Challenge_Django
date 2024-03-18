from sqlalchemy import text, insert, select
from database.database import engine, session_factory, Base
from database.models import DateOrm, ExchangeOrm


class OrmMethods:
    @staticmethod
    async def create_tables():
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def delete_tables():
        async with engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.commit()

    @staticmethod
    async def add_new_data(model, attributes):
        async with session_factory() as session:
            async with session.begin():
                data = await session.execute(select(model).filter_by(**attributes))
                data = data.scalars().first()
                if data is None:
                    new_data = model(**attributes)
                    session.add(new_data)
                    await session.flush()  # Fix changes to get an id of a new data
                    return new_data.id
