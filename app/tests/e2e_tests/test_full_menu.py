from typing import Any
from httpx import AsyncClient


async def test_add_menu(ac: AsyncClient, save_data: dict[str, Any]):
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
    save_data["menu_id"] = response.json()["id"]


async def test_add_submenu(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.post(
        f"/menus/{save_data['menu_id']}/submenus",
        json={
            "title": "Submenu 1 title",
            "description": "Submenu 1 description",
        },
    )
    assert response.status_code == 201, "Подменю не было создано"
    assert "id" in response.json()
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"
    save_data["submenu_id"] = response.json()["id"]


async def test_add_dish(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.post(
        f"/menus/{save_data['menu_id']}/submenus/{save_data['submenu_id']}/dishes",
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
    save_data["first_dish_id"] = response.json()["id"]


async def test_add_second_dish(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.post(
        f"/menus/{save_data['menu_id']}/submenus/{save_data['submenu_id']}/dishes",
        json={
            "title": "My dish 2",
            "description": "My dish 2 description",
            "price": 14.45,
        },
    )
    assert response.status_code == 201, "Блюдо не было создано"
    assert response.json()["title"] == "My dish 2"
    assert response.json()["description"] == "My dish 2 description"
    assert response.json()["price"] == "14.45"
    save_data["second_dish_id"] = response.json()["id"]


async def test_get_menu_by_id(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.get(f"/menus/{save_data['menu_id']}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == str(save_data["menu_id"])
    assert response.json()["title"] == "Menu 1 title"
    assert response.json()["description"] == "Menu 1 description"
    assert response.json()["submenus_count"] == 1
    assert response.json()["dishes_count"] == 2


async def test_get_submenu_by_id(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.get(
        f"/menus/{save_data['menu_id']}/submenus/{save_data['submenu_id']}"
    )
    assert response.status_code == 200, "Такого подменю нет"
    assert response.json()["id"] == str(save_data["submenu_id"])
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"


async def test_delete_submenu(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.delete(
        f"/menus/{save_data['menu_id']}/submenus/{save_data['submenu_id']}"
    )
    assert response.status_code == 200, "Удаление подменю не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The submenu has been deleted"


async def test_get_submenu_list(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.get(f"/menus/{save_data['menu_id']}/submenus")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_dishes_list(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.get(
        f"/menus/{save_data['menu_id']}/submenus/{save_data['submenu_id']}/dishes"
    )
    assert response.status_code == 200
    assert response.json() == []


async def test_get_menu_after_remove_sd(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.get(f"/menus/{save_data['menu_id']}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == str(save_data["menu_id"])
    assert response.json()["title"] == "Menu 1 title"
    assert response.json()["description"] == "Menu 1 description"
    assert response.json()["submenus_count"] == 0
    assert response.json()["dishes_count"] == 0


async def test_delete_menu(ac: AsyncClient, save_data: dict[str, Any]):
    response = await ac.delete(f"/menus/{save_data['menu_id']}")
    assert response.status_code == 200, "Удаление меню не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The menu has been deleted"


async def test_get_removed_menu(ac: AsyncClient):
    response = await ac.get(f"/menus")
    assert response.status_code == 200, "В списке есть какие-то меню"
    assert response.json() == []
