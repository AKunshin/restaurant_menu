from loguru import logger
from sqlalchemy import func, select, join
from app.database import async_session_maker
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


async def get_menu_with_counts(id):
    async with async_session_maker() as session:
        """
        SELECT M.TITLE,
        M.DESCRIPTION,
        COUNT(S.ID) AS SUBMENUS_COUNT,
        COUNT(D.ID) AS DISHES_COUNT
        FROM MENUS AS M
        JOIN SUBMENUS AS S ON S.MENU_ID = M.ID
        JOIN DISHES AS D ON D.SUBMENU_ID = S.ID
        WHERE M.ID = '1150a2e8-1aa6-49c8-a562-f0903dcfd990'
        GROUP BY M.ID;
        """
        j = join(Menu, Submenu, Menu.id == Submenu.menu_id, isouter=True)
        stmt = select(Menu).select_from(j)

        result = await session.execute(stmt)
        # result = result.scalars()
        # logger.debug(f"{result=}")
        return result.scalars().all()
