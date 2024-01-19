from sqlalchemy import insert, select
from pydantic import UUID4

from app.database import async_session_maker

class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model) 
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def get_by_id(cls, model_id: UUID4):
        async with async_session_maker() as session:
            query =select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()