from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, status
from loguru import logger
from pydantic import UUID4


from app.menu.dao import MenuDAO
from app.menu.schemas import SMenuCreate, SMenu, SMenuUpdate, SMenuUpdatePartial

router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)


@router.get("", response_model=list[SMenu])
async def get_menus():
    result = await MenuDAO.get_all()
    return list(result)


@router.get("/{target_menu_id}", response_model=SMenu | None)
async def get_menu_by_id(target_menu_id: Annotated[UUID4, Path]):
    result = await MenuDAO.get_by_id(id=target_menu_id)
    if result:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="menu not found"
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=SMenu)
async def add_menu(new_menu: SMenuCreate):
    data = new_menu.model_dump()
    return await MenuDAO.add_item(data)

@router.patch("/{target_menu_id}", response_model=SMenu)
async def update_menu(target_menu_id: Annotated[UUID4, Path], menu_update: SMenuUpdatePartial):
    updated_menu = await MenuDAO.update_item(menu_update, id=target_menu_id)
    return updated_menu

@router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: Annotated[UUID4, Path]):
    is_menu_deleted = await MenuDAO.delete_item(id=target_menu_id)
    if not is_menu_deleted:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="menu not found"
    )
    return {"status": "true", "message": "The menu has been deleted"}
