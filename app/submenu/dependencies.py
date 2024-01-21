from typing import Annotated
from fastapi import Depends, HTTPException, Path, status
from loguru import logger
from pydantic import UUID4
from app.menu.dependencies import get_menu
from app.menu.models import Menu

from app.submenu.dao import SubmenuDAO
from app.submenu.models import Submenu


async def get_submenu(
    target_submenu_id: Annotated[UUID4, Path] | None = None,
    menu: Menu = Depends(get_menu),
) -> Submenu:
    """Получение определенного подменю"""
    logger.debug(f"{target_submenu_id=}")
    if not target_submenu_id:
        submenu = await SubmenuDAO.get_by_id(menu_id=menu.id, id=target_submenu_id)
        if submenu is not None:
            return submenu
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
    )
