from sqlalchemy import select, insert, delete, update
from fastapi import APIRouter, HTTPException, status

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
    async def update_item(cls, update_values, **filter_by):
        async with async_session_maker() as session:
            # stmt = update(cls.model).values(update_values).where(**filter_by)
            # updated_item = await session.execute(stmt)
            # return updated_item


            query = select(cls.model).filter_by(**filter_by)
            updated_item = await session.execute(query)
            # TODO
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            deleting_item = result.scalar_one_or_none()
            if deleting_item:
                await session.delete(deleting_item)
                await session.commit()
                return True
            else:
                return False
            
            for name, value in update_values.model_dump(exclude_unset=partial).items():
                setattr(updated_item, name, value)
            await session.commit()
            await session.refresh(updated_item)
            return updated_item

    @classmethod
    async def delete_item(cls, item_id):
        async with async_session_maker() as session:
            deleting_item = await session.get(cls.model, item_id)
            if deleting_item:
                await session.delete(deleting_item)
                await session.commit()
                return True
            else:
                return False
            
