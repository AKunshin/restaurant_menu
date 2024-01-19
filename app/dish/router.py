from fastapi import APIRouter
from pydantic import UUID4


from app.dish.dao import DishDAO
from app.dish.schemas import SDish

router = APIRouter(
    prefix="/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    tags=["Блюдо"],
)


@router.get("")
async def get_dishes() -> list[SDish]:
    return await DishDAO.get_all()


@router.get("/{model_id}", response_model=SDish)
async def get_menu_by_id(model_id: UUID4):
    return await DishDAO.get_by_id(model_id=model_id)
