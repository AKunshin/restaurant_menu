from loguru import logger
from sqlalchemy import select, delete

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
    async def add_item(cls, insert_values):
        async with async_session_maker() as session:
            new_item = cls.model(**insert_values)
            session.add(new_item)
            await session.commit()
            await session.refresh(new_item)
            return new_item

    @classmethod
    async def update_item(cls, update_values: dict, **filter_by):
        async with async_session_maker() as session:
            updating_item = await cls.get_by_id(**filter_by)
            for name, value in update_values.model_dump(exclude_unset=True).items():
                setattr(updating_item, name, value)
            session.add(updating_item)
            await session.commit()
            await session.refresh(updating_item)
            return updating_item

    @classmethod
    async def delete_item(cls, **filter_by):
        async with async_session_maker() as session:
            deleting_item = await cls.get_by_id(**filter_by)
            if deleting_item:
                await session.delete(deleting_item)
                await session.commit()
                return True
            else:
                return False
