from typing import Annotated
from fastapi import Depends, HTTPException, Path, status
from pydantic import UUID4
from app.dish.dao import DishDAO
from app.dish.models import Dish
from app.submenu.dependencies import get_submenu

from app.submenu.models import Submenu


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
