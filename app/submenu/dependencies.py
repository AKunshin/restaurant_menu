from 

async def get_submenu_by_id(
    target_menu_id: Annotated[UUID4, Path], target_submenu_id: Annotated[UUID4, Path]
):
    """Получение определенного подменю"""
    result = await SubmenuDAO.get_by_id(menu_id=target_menu_id, id=target_submenu_id)
    return result