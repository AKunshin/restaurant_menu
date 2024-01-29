from loguru import logger
from sqlalchemy import UUID, func, select, join
from app.database import async_session_maker
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


async def get_menu_with_counts(id):
    async with async_session_maker() as session:
        """
        SELECT MENUS.ID,
        MENUS.TITLE,
        MENUS.DESCRIPTION,
        COUNT(SUBMENUS.MENU_ID = '4aed8d67-2c93-4280-8386-5603a52243a9') AS SUBMENUS_COUNT,
        COUNT(SUBMENUS.ID = DISHES.SUBMENU_ID) FILTER (
        WHERE SUBMENUS.MENU_ID = '4aed8d67-2c93-4280-8386-5603a52243a9') AS DISHES_COUNT
        FROM MENUS
        JOIN SUBMENUS ON MENUS.ID = SUBMENUS.MENU_ID
        JOIN DISHES ON SUBMENUS.ID = DISHES.SUBMENU_ID
        WHERE MENUS.ID = '4aed8d67-2c93-4280-8386-5603a52243a9'
            AND SUBMENUS.MENU_ID = '4aed8d67-2c93-4280-8386-5603a52243a9'
        GROUP BY MENUS.ID

        SELECT
        (SELECT COUNT(SUBMENUS.ID) AS COUNT_1
            FROM SUBMENUS
            WHERE SUBMENUS.MENU_ID = MENUS.ID) AS ANON_1,

        (SELECT
                (SELECT COUNT(DISHES.ID) AS COUNT_2
                    FROM DISHES,
                        SUBMENUS
                    WHERE DISHES.SUBMENU_ID = SUBMENUS.ID) AS ANON_3) AS ANON_2,
        MENUS.ID,
        MENUS.TITLE,
        MENUS.DESCRIPTION
        FROM MENUS
        WHERE MENUS.ID = '4aed8d67-2c93-4280-8386-5603a52243a9'




        """
        # subq1 = (
        #     select(func.count(Submenu.id)
        #     .where(Submenu.menu_id == id))
        #     .join(Menu.submenus)
        #     .label("submenus_count")
        #     .subquery("helper1"))
        # subq2 = (
        #     select(func.count(Dish.id))
        #     .where(Dish.submenu_id == id)
        #     .join(Submenu.dishes)
        #     .label("dishes_count")
        #     .subquery("helper2")
        # )
        # cte = (
        #     subq1.c.id,
        #     subq1.c.title,
        #     subq1.c.description,
        #     subq

        # )
        stmt = (
            select(Menu)
            .add_columns(func.count(Submenu.menu_id).label("submenus_count"))
            .add_columns(
                func.count(Dish.submenu_id).label("dishes_count")
            )
            .join(Menu.submenus)
            .join(Submenu.dishes)
            .filter(Menu.id == id)
            .group_by(Menu.id)
        )

        result = await session.execute(stmt)
        # result = result.scalars()
        # logger.debug(f"{result=}")
        return result.scalars().all()
