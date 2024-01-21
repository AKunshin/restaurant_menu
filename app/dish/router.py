from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status
from pydantic import UUID4


from app.dish.dao import DishDAO
from app.dish.schemas import SDish, SDishCreate, SDishUpdate, SDishUpdatePartial

router = APIRouter(
    prefix="/dishes",
    tags=["Блюдо"],
)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_dishes(
    target_menu_id: Annotated[UUID4, Path], target_submenu_id: Annotated[UUID4, Path]
) -> list[SDish]:
    return await DishDAO.get_all(submenu_id=target_submenu_id)


@router.get("/{model_id}", response_model=SDish)
async def get_menu_by_id(model_id: UUID4):
    return await DishDAO.get_by_id(model_id=model_id)
