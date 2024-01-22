from typing import Annotated
from fastapi import Depends, HTTPException, Path, status
from pydantic import UUID4


from app.menu.dependencies import get_menu
from app.menu.models import Menu
from app.dish.dao import DishDAO
from app.dish.models import Dish
from app.submenu.dao import SubmenuDAO
from app.submenu.dependencies import get_submenu

from app.submenu.models import Submenu


async def get_submenu_or_empty(
    target_submenu_id: Annotated[UUID4, Path],
    menu: Menu = Depends(get_menu),
) -> Submenu:
    """Получение определенного подменю или пусто"""
    submenu = await SubmenuDAO.get_by_id(menu_id=menu.id, id=target_submenu_id)
    return submenu

async def get_dish(
    target_dish_id: Annotated[UUID4, Path],
    submenu: Submenu = Depends(get_submenu),
) -> Dish:
    """Получение определенного блюда"""
    dish = await DishDAO.get_by_id(submenu_id=submenu.id, id=target_dish_id)
    if dish is not None:
        return dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
    )
