from pydantic import UUID4
from sqlalchemy import distinct, func, select


from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.menu.models import Menu
from app.submenu.models import Submenu


class MenuDAO(BaseDAO):
    model = Menu

    @classmethod
    async def get_all_menu_fields_by_id(cls, id: UUID4=id):
        """
        Получение объекта меню с количеством подменю и блюд,
        с помощью одного ORM запроса
        """
        async with async_session_maker() as session:

            stmt = (
                select(
                    Menu.id,
                    Menu.title,
                    Menu.description,
                    func.count(distinct(Submenu.id)).label("submenus_count"),
                    func.count(Submenu.dishes).label("dishes_count"),
                )
                .join(Menu.submenus)
                .join(Submenu.dishes)
                .filter(Menu.id == id)
                .group_by(Menu.id)
            )
            result = await session.execute(stmt)
            return result.mappings().one_or_none()
