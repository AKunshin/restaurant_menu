from fastapi import APIRouter
from pydantic import UUID4


from app.menu.dao import MenuDAO
from app.menu.models import Menu
from app.menu.schemas import SMenus

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menus() -> list[SMenus]:
    return await MenuDAO.get_all()


@router.get("/{model_id}")
async def get_menu_by_id(model_id: UUID4) -> SMenus:
    return await MenuDAO.get_by_id(model_id=model_id)
