from typing import Annotated
from fastapi import APIRouter, Depends, Path, status
from pydantic import UUID4


from app.submenu.dao import SubmenuDAO
from app.submenu.dependencies import get_submenu
from app.submenu.models import Submenu
from app.submenu.schemas import (
    SSubmenu,
    SSubmenuCreate,
    SSubmmenuUpdatePartial,
)

router = APIRouter(
    prefix="/menus",
    tags=["Подменю"],
)


@router.get("/{target_menu_id}/submenus")
async def get_submenus_for_menu(
    target_menu_id: Annotated[UUID4, Path]
) -> list[SSubmenu] | None:
    """Получение списка всех подменю для определенного меню"""
    result = await SubmenuDAO.get_all(menu_id=target_menu_id)
    return result


@router.get("/{target_menu_id}/submenus/{target_submenu_id}", response_model=SSubmenu)
async def get_submenu_by_id(
    submenu: Submenu = Depends(get_submenu),
):
    """Получение определенного подменю"""
    return submenu


@router.post(
    "/{target_menu_id}/submenus/",
    status_code=status.HTTP_201_CREATED,
    response_model=SSubmenu,
)
async def add_submenu(
    target_menu_id: Annotated[UUID4, Path], new_submenu: SSubmenuCreate
):
    """Создание нового подменю"""
    data = new_submenu.model_dump()
    data.update(menu_id=target_menu_id)
    return await SubmenuDAO.add_item(data)


@router.patch(
    "/{target_menu_id}/submenus/{target_submenu_id}", response_model=SSubmenu | None
)
async def update_submenu_partial(
    submenu_update: SSubmmenuUpdatePartial,
    submenu: Submenu = Depends(get_submenu)
):
    """Частичное обновление подменю"""
    updated_submenu = await SubmenuDAO.update_item(
        updating_item=submenu,
        update_values=submenu_update,
    )
    return updated_submenu

@router.delete("/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_submenu(submenu: Submenu = Depends(get_submenu)):
    """Удаление подменю"""
    await SubmenuDAO.delete_item(submenu)
    return {"status": "true", "message": "The submenu has been deleted"}
