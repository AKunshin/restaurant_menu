from httpx import AsyncClient
import pytest


async def test_add_menu(ac: AsyncClient):
    response = await ac.post(
        "/menus",
        json={
            "title": "Menu 1 title",
            "description": "Menu 1 description",
        },
    )
    assert response.status_code == 201, "Меню не было создано"
    assert "id" in response.json()
    assert response.json()["title"] == "Menu 1 title"
    assert response.json()["description"] == "Menu 1 description"


async def test_add_submenu(ac: AsyncClient, get_mock_menu):
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


async def test_add_dish(get_mock_menu_for_test_delete, get_mock_submenu_for_test_delete, ac: AsyncClient):
    response = await ac.post(
        f"/menus/{get_mock_menu_for_test_delete.id}/submenus/{get_mock_submenu_for_test_delete.id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish 1 description",
            "price": 12.345,
        },
    )
    assert response.status_code == 201, "Блюдо не было создано"
    assert response.json()["title"] == "My dish 1"
    assert response.json()["description"] == "My dish 1 description"
    assert response.json()["price"] == "12.35"


async def test_add_second_dish(get_mock_menu_for_test_delete, get_mock_submenu_for_test_delete, ac: AsyncClient):
    response = await ac.post(
        f"/menus/{get_mock_menu_for_test_delete.id}/submenus/{get_mock_submenu_for_test_delete.id}/dishes",
        json={
            "title": "My dish 2",
            "description": "My dish 2 description",
            "price": 14.45,
        },
    )
    assert response.status_code == 201, "Блюдо не было создано"
    assert response.json()["title"] == "My dish 1"
    assert response.json()["description"] == "My dish 1 description"
    assert response.json()["price"] == "12.35"


async def test_get_menu_by_id(ac: AsyncClient, get_mock_menu_for_test_delete):
    response = await ac.get(f"/menus/{get_mock_menu_for_test_delete.id}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == str(get_mock_menu_for_test_delete.id)
    assert response.json()["title"] == get_mock_menu_for_test_delete.title
    assert response.json()["description"] == get_mock_menu_for_test_delete.description
    assert response.json()["submenus_count"] == 2
    assert response.json()["dishes_count"] == 2


async def test_get_submenu_by_id(ac: AsyncClient, get_mock_menu_for_test_delete, get_mock_submenu):
    response = await ac.get(f"/menus/{get_mock_menu_for_test_delete.id}/submenus/{get_mock_submenu.id}")
    assert response.status_code == 200, "Такого подменю нет"
    assert response.json()["id"] == str(get_mock_submenu.id)
    assert response.json()["title"] == get_mock_submenu.title
    assert response.json()["description"] == get_mock_submenu.description


async def test_delete_submenu(
    ac: AsyncClient, get_mock_menu, get_mock_submenu_for_test_delete
):
    response = await ac.delete(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu_for_test_delete.id}"
    )
    assert response.status_code == 200, "Удаление подменю не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The submenu has been deleted"


async def test_get_submenu_list(ac: AsyncClient, get_mock_menu, get_mock_submenu):
    response = await ac.get(f"/menus/{get_mock_menu.id}/submenus")
    assert response.status_code == 200, "Списка подменю для этого меню нет"
    assert response.json()["id"] == str(get_mock_submenu.id)
    assert response.json()["title"] == get_mock_submenu.title
    assert response.json()["description"] == get_mock_submenu.description


async def test_full_menu(
    ac: AsyncClient, get_mock_menu, get_mock_submenu, get_mock_dish
):
    response = await ac.get(f"menus/{get_mock_menu.id}")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == get_mock_menu.title
    assert response.json()["description"] == get_mock_menu.description
