from loguru import logger
from sqlalchemy import func, select
from app.database import async_session_maker
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


async def get_menu_with_counts(id):
    async with async_session_maker() as session:
        """
        select count(id) as submenus_count
        from submenus
        where menu_id='1150a2e8-1aa6-49c8-a562-f0903dcfd990';
         SELECT count(submenus.id) AS submenus_count
        FROM submenus
        WHERE submenus.menu_id = $1::UUID
        """
        stmt = select(func.count(Submenu.id).label("submenus_count")).filter(Submenu.menu_id == id)


        result = await session.execute(stmt)
        result = result.scalar_one()
        logger.debug(f"{result=}")
        return result
