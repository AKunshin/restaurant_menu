from typing import Annotated
from fastapi import HTTPException, Path, status
from pydantic import UUID4
from app.menu.dao import MenuDAO

from app.menu.models import Menu


async def get_menu(target_menu_id: Annotated[UUID4, Path]) -> Menu:
    """Получение определенного меню"""
    menu = await MenuDAO.get_by_id(id=target_menu_id)
    if menu is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")


async def get_menu_by_one_select(target_menu_id: Annotated[UUID4, Path]) -> Menu:
    """Получение определенного меню"""
    menu = await MenuDAO.get_all_menu_fields_by_id(id=target_menu_id)
    if menu is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
