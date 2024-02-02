from loguru import logger
from sqlalchemy import Integer, and_, distinct, func, select, join, cast
from sqlalchemy.orm import aliased


from app.database import async_session_maker
from app.dao.base import BaseDAO
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


class MenuDAO(BaseDAO):
    model = Menu

    @classmethod
    async def get_all_menu_fields_by_id(cls, id=id):
        async with async_session_maker() as session:
            """
            SELECT MENUS.ID,
            MENUS.TITLE,
            MENUS.DESCRIPTION,
            COUNT(DISTINCT SUBMENUS.ID) AS SUBMENUS_COUNT,
            COUNT(SUBMENUS.ID = DISHES.SUBMENU_ID) AS DISHES_COUNT
            FROM MENUS
            JOIN SUBMENUS ON MENUS.ID = SUBMENUS.MENU_ID
            JOIN DISHES ON SUBMENUS.ID = DISHES.SUBMENU_ID
            WHERE MENUS.ID = '4aed8d67-2c93-4280-8386-5603a52243a9'
            GROUP BY MENUS.ID
            """
            stmt = (
                select(
                    Menu,
                    func.count(distinct(Submenu.id)).label("submenus_count"),
                    func.count(Submenu.dishes).label("dishes_count"),
                )
                .join(Menu.submenus)
                .join(Submenu.dishes)
                .filter(Menu.id == id)
                .group_by(Menu.id, Submenu.id)
            )
            result = await session.execute(stmt)
            return result.mappings().all()
