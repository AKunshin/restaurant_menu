from fastapi import APIRouter, Depends, status


from app.menu.dao import MenuDAO
from app.menu.dependencies import get_menu
from app.menu.models import Menu
from app.menu.schemas import SMenuCreate, SMenu, SMenuUpdatePartial

from app.menu.utils import get_menu_with_counts



router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)

@router.get("/test/{target_menu_id}",
            )
async def get_menu_with_sd(target_menu_id):
    result = await get_menu_with_counts(target_menu_id)
    return result


@router.get("", response_model=list[SMenu])
async def get_menus():
    """Получение списка всех меню"""
    result = await MenuDAO.get_all()
    return list(result)


@router.get("/{target_menu_id}", response_model=SMenu)
async def get_menu_by_id(menu: Menu = Depends(get_menu)):
    """Получение определенного подменю"""
    return menu


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SMenu)
async def add_menu(new_menu: SMenuCreate):
    """Создание нового меню"""
    data = new_menu.model_dump()
    return await MenuDAO.add_item(data)


@router.patch("/{target_menu_id}", response_model=SMenu)
async def update_menu(
    menu_update: SMenuUpdatePartial,
    menu: Menu = Depends(get_menu),
):
    """Частичное или полное обновление полей меню"""
    updated_menu = await MenuDAO.update_item(
        updating_item=menu, update_values=menu_update
    )
    return updated_menu


@router.delete("/{target_menu_id}")
async def delete_menu(menu: Menu = Depends(get_menu)):
    """Удаление меню"""
    await MenuDAO.delete_item(menu)
    return {"status": "true", "message": "The menu has been deleted"}
