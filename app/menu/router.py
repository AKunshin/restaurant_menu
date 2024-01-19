from fastapi import APIRouter
from pydantic import UUID4


from app.menu.dao import MenuDAO
from app.menu.schemas import SMenus

router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menus() -> list[SMenus]:
    return await MenuDAO.get_all()


@router.get("/{target_menu_id}")
async def get_menu_by_id(target_menu_id: UUID4) -> SMenus | None:
    return await MenuDAO.get_by_id(id=target_menu_id)
