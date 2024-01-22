from fastapi import APIRouter, Depends, status


from app.dish.dao import DishDAO
from app.dish.dependencies import get_dish
from app.dish.models import Dish
from app.dish.schemas import SDish, SDishCreate, SDishUpdatePartial
from app.submenu.dependencies import get_submenu
from app.submenu.models import Submenu

router = APIRouter(
    prefix="/menus",
    tags=["Блюдо"],
)


@router.get(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes", response_model=list[SDish]
)
async def get_dishes(submenu: Submenu = Depends(get_submenu)):
    """Получение списка блюд для определенного подменю"""
    result = await DishDAO.get_all(submenu_id=submenu.id)
    return list(result)


@router.get(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    response_model=SDish,
)
async def get_dish_by_id(dish: Dish = Depends(get_dish)):
    """Получение определенного блюда"""
    return dish


@router.post(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes",
    status_code=status.HTTP_201_CREATED,
    response_model=SDish,
)
async def add_dish(
    new_dish: SDishCreate,
    submenu: Submenu = Depends(get_submenu),
):
    """Создание нового блюда"""
    data = new_dish.model_dump()
    data.update(submenu_id=submenu.id)
    return await DishDAO.add_item(data)


@router.patch(
    "/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
    response_model=SDishUpdatePartial,
)
async def update_submenu_partial(
    dish_update: SDishUpdatePartial, dish: Dish = Depends(get_dish)
):
    """Частичное обновление блюда"""
    updated_dish = await DishDAO.update_item(
        updating_item=dish,
        update_values=dish_update,
    )
    return updated_dish


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def delete_submenu(dish: Dish = Depends(get_dish)):
    """Удаление блюда"""
    await DishDAO.delete_item(dish)
    return {"status": "true", "message": "The dish has been deleted"}
