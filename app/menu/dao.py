from sqlalchemy import Integer, distinct, func, select, join, cast


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
            stmt = (
                select(Menu)
                .add_columns(
                    func.count(distinct(Menu.submenus)).cast(Integer).label(
                        "submenus_count"
                    )
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
