from fastapi import APIRouter
from pydantic import UUID4


from app.submenu.dao import SubmenuDAO
from app.submenu.schemas import SSubmenus

router = APIRouter(
    prefix="/menus/{target_menu_id}/submenus",
    tags=["Подменю"],
)


@router.get("")
async def get_submenus() -> list[SSubmenus]:
    return await SubmenuDAO.get_all()


@router.get("/{model_id}", response_model=SSubmenus)
async def get_menu_by_id(model_id: UUID4):
    return await SubmenuDAO.get_by_id(model_id=model_id)
