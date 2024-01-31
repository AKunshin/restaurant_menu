from httpx import AsyncClient

from app.menu.models import Menu
from app.submenu.models import Submenu


async def test_add_submenu(ac: AsyncClient, get_mock_menu: Menu):
    response = await ac.post(
        f"/menus/{get_mock_menu.id}/submenus",
        json={
            "title": "Submenu 1 title",
            "description": "Submenu 1 description",
        },
    )
    assert response.status_code == 201, "Подменю не было создано"
    assert "id" in response.json()
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"


async def test_get_submenu_by_id(
    ac: AsyncClient, get_mock_menu: Menu, get_mock_submenu: Submenu
):
    response = await ac.get(f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}")
    assert response.status_code == 200, "Указанное подменю не найдено"
    assert response.json()["id"] == str(get_mock_submenu.id)
    assert response.json()["title"] == get_mock_submenu.title
    assert response.json()["description"] == get_mock_submenu.description


async def test_update_menu(
    ac: AsyncClient, get_mock_menu: Menu, get_mock_submenu: Submenu
):
    response = await ac.patch(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}",
        json={
            "title": "Updated Submenu 1 title",
            "description": "Updated Submenu 1 description",
        },
    )
    assert response.status_code == 200, "Обновление подменю не выполнено"
    assert response.json()["id"] == str(get_mock_submenu.id)
    assert response.json()["title"] == "Updated Submenu 1 title"
    assert response.json()["description"] == "Updated Submenu 1 description"


async def test_delete_menu(
    ac: AsyncClient, get_mock_menu: Menu, get_mock_submenu_for_test_delete: Submenu
):
    response = await ac.delete(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu_for_test_delete.id}"
    )
    assert response.status_code == 200, "Удаление подменю не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The submenu has been deleted"


async def test_get_removed_submenu(
    ac: AsyncClient, get_mock_menu: Menu, get_mock_submenu_for_test_delete: Submenu
):
    response = await ac.get(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu_for_test_delete.id}"
    )
    assert (
        response.status_code == 404
    ), "Подменю, которое должно было быть удалено, все еще существует"
