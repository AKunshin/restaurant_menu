from sqlalchemy import Result, insert, select
from loguru import logger

from app.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def get_by_id(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, insert_values):
        async with async_session_maker() as session:
            new_item = cls.model(**insert_values)
            session.add(new_item)
            await session.commit()
            return new_item
            # query = insert(cls.model).values(insert_values)
            # result  = await session.execute(query)
            # await session.commit()
            # return result.scalar()