from sqlalchemy import select

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
    async def update_item(cls, updating_item, update_values):
        async with async_session_maker() as session:
            for name, value in update_values.model_dump(exclude_unset=True).items():
                setattr(updating_item, name, value)
            session.add(updating_item)
            await session.commit()
            await session.refresh(updating_item)
            return updating_item

    @classmethod
    async def delete_item(cls, item):
        async with async_session_maker() as session:
            await session.delete(item)
            await session.commit()
