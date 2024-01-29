from sqlalchemy import distinct, func, select, join, Integer

from app.database import async_session_maker
from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


async def get_menu_with_counts(id):
    async with async_session_maker() as session:
        stmt = (
            select(Menu)
            .add_columns(
                func.count(distinct(Menu.submenus))
                .cast(Integer)
                .label("submenus_count")
            )
            .add_columns(
                func.count(Dish.submenu_id).cast(Integer).label("dishes_count")
            )
            .join(Menu.submenus)
            .join(Submenu.dishes)
            .filter(Menu.id == id)
            .group_by(Menu.id)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()
