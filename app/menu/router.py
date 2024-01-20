from fastapi import APIRouter, Body
from loguru import logger
from pydantic import UUID4
from typing import Annotated


from app.menu.dao import MenuDAO
from app.menu.schemas import SMenuCreate, SMenus

router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menus() -> list[SMenus]:
    result = await MenuDAO.get_all()
    return list(result)


@router.get("/{target_menu_id}")
async def get_menu_by_id(target_menu_id: UUID4) -> SMenus | None:
    result = await MenuDAO.get_by_id(id=target_menu_id)
    return result


@router.post("", status_code=201, response_model=SMenus)
async def add_menu(new_menu: SMenuCreate):
    data = new_menu.model_dump()
    return await MenuDAO.add_item(data)
