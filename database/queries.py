from sqlalchemy import text, insert, select, and_
from sqlalchemy.orm import joinedload, load_only
from database.database import engine, session_factory, Base
from database.models import DateOrm, ExchangeOrm, InstrumentOrm


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

    @staticmethod
    async def find_data(search_conditions: list):
        async with session_factory() as session:
            instrument_load_list = [InstrumentOrm.name, InstrumentOrm.iid, InstrumentOrm.storage_type]
            query = (select(InstrumentOrm)
                     .join(InstrumentOrm.exchange)
                     .join(ExchangeOrm.date)
                     .options(joinedload(InstrumentOrm.exchange)
                              .load_only(ExchangeOrm.name)
                              )
                     .options(load_only(*instrument_load_list))
                     .filter(and_(*search_conditions))
                     )

            result = await session.execute(query)
            data = result.scalars().all()
            return data
