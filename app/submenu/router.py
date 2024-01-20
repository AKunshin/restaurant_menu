from fastapi import APIRouter, HTTPException, status
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
async def get_submenus(target_menu_id: UUID4) -> list[SSubmenu] | None:
    result = await SubmenuDAO.get_all(menu_id=target_menu_id)
    return result


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_menu_by_id(
    target_menu_id: UUID4, target_submenu_id: UUID4
) -> SSubmenu | None:
    result = await SubmenuDAO.get_by_id(menu_id=target_menu_id, id=target_submenu_id)
    return result


@router.post("/{target_menu_id}/submenus/", status_code=201, response_model=SSubmenu)
async def add_menu(target_menu_id: UUID4, new_submenu: SSubmenuCreate):
    data = new_submenu.model_dump()
    data.update(menu_id=target_menu_id)
    return await SubmenuDAO.add_item(data)


@router.patch(
    "/{target_menu_id}/submenus/{target_submenu_id}", response_model=SSubmenu | None
)
async def update_menu(
    target_menu_id: UUID4,
    target_submenu_id: UUID4,
    submenu_update: SSubmmenuUpdate | SSubmmenuUpdatePartial,
):
    update_values = submenu_update.model_dump()
    update_values.update(menu_id=target_menu_id)
    updated_submenu = await SubmenuDAO.update_item(
        update_values, menu_id=target_menu_id, id=target_submenu_id
    )
    return updated_submenu


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_menu(target_menu_id: UUID4, target_submenu_id: UUID4):
    is_menu_deleted = await SubmenuDAO.delete_item(
        menu_id=target_menu_id, id=target_submenu_id
    )
    if not is_menu_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    return {"status": "true", "message": "The submenu has been deleted"}
