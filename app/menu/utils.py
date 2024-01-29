from loguru import logger
from sqlalchemy import distinct, func, select, join
from app.database import async_session_maker
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


async def get_menu_with_counts(id):
    async with async_session_maker() as session:
        stmt = (
            select(Menu)
            .add_columns(func.count(distinct(Menu.submenus)).label("submenus_count"))
            .add_columns(
                func.count(Dish.submenu_id).label("dishes_count")
            )
            .join(Submenu.dishes)
            .filter(Menu.id == id)
            .group_by(Menu.id)
        )

        result = await session.execute(stmt)
        logger.debug(f"{result=}")
        return result.scalar_one_or_none()
