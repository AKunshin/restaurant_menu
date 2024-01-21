from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status
from pydantic import UUID4


from app.submenu.dao import SubmenuDAO
from app.submenu.schemas import (
    SSubmenu,
    SSubmenuCreate,
    SSubmmenuUpdate,
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


@router.get(
    "/{target_menu_id}/submenus/{target_submenu_id}", response_model=SSubmenu | None
)
async def get_submenu_by_id(
    target_menu_id: Annotated[UUID4, Path], target_submenu_id: Annotated[UUID4, Path]
):
    """Получение определенного подменю"""
    result = await SubmenuDAO.get_by_id(menu_id=target_menu_id, id=target_submenu_id)
    return result


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
    target_menu_id: Annotated[UUID4, Path],
    target_submenu_id: Annotated[UUID4, Path],
    submenu_update: SSubmmenuUpdatePartial,
):
    """Частичное обновление подменю"""
    updated_submenu = await SubmenuDAO.update_item(
        submenu_update, menu_id=target_menu_id, id=target_submenu_id
    )
    return updated_submenu


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_menu(
    target_menu_id: Annotated[UUID4, Path], target_submenu_id: Annotated[UUID4, Path]
):
    """Удаление подменю"""
    is_menu_deleted = await SubmenuDAO.delete_item(
        menu_id=target_menu_id, id=target_submenu_id
    )
    if not is_menu_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return {"status": "true", "message": "The submenu has been deleted"}
