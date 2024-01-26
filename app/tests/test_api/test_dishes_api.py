from httpx import AsyncClient
import pytest

target_menu_id = None
target_submenu_id = None
target_dish_id = None


async def test_add_menu(ac: AsyncClient):
    response = await ac.post(
        "/menus",
        json={
            "title": "Menu 1 title",
            "description": "Menu 1 description",
        },
    )
    assert response.status_code == 201, "Меню не было создано"
    global target_menu_id
    target_menu_id = response.json()["id"]


async def test_add_submenu(ac: AsyncClient):
    response = await ac.post(
        f"/menus/{target_menu_id}/submenus",
        json={
            "title": "Submenu 1 title",
            "description": "Submenu 1 description",
        },
    )
    assert response.status_code == 201, "Подменю не было создано"
    global target_submenu_id
    target_submenu_id = response.json()["id"]


@pytest.mark.parametrize(
    "title, description, price",
    [
        ("Dish 1 title", "Dish 1 description", 11.23),
        # ("Dish 2 title", "Dish 2 description", 22.26),
    ],
)
async def test_add_dish(title, description, price, ac: AsyncClient):
    response = await ac.post(f"/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
    assert response.status_code == 201, "Блюдо не было создано"
    assert response.json()["title"] == title
    assert response.json()["description"] == description
    assert response.json()["price"] == price
    global target_dish_id
    target_dish_id = response.json()["id"]


async def test_get_dish_by_id(ac: AsyncClient):
    response = await ac.get(
        f"/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}"
    )
    assert response.status_code == 200, "Такого блюда нет"
    assert response.json()["id"] == target_dish_id
    assert response.json()["title"] == "Dish 1 title"
    assert response.json()["description"] == "Dish 1 description"


async def test_update_dish(ac: AsyncClient):
    response = await ac.patch(
        f"/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
        json={
            "title": "Updated Dish 1 title",
            "description": "Updated Dish 1 description",
        },
    )
    assert response.status_code == 200, "Обновление блюда не выполнено"
    assert response.json()["id"] == target_dish_id
    assert response.json()["title"] == "Updated Dish 1 title"
    assert response.json()["description"] == "Updated Dish 1 description"


async def test_delete_dish(ac: AsyncClient):
    response = await ac.delete(f"/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
    assert response.status_code == 200, "Удаление блюда не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The dish has been deleted"
