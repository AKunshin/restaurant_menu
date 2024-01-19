from fastapi import APIRouter
from pydantic import UUID4


from app.submenu.dao import SubmenuDAO
from app.submenu.schemas import SSubmenus

router = APIRouter(
    prefix="/menus",
    tags=["Подменю"],
)


@router.get("/{target_menu_id}/submenus")
async def get_submenus(target_menu_id: UUID4) -> list[SSubmenus] | None:
    result = await SubmenuDAO.get_all(menu_id=target_menu_id)
    return result


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_menu_by_id(
    target_menu_id: UUID4, target_submenu_id: UUID4
) -> SSubmenus | None:
    result = await SubmenuDAO.get_by_id(menu_id=target_menu_id, id=target_submenu_id)
    return result
