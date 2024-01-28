from decimal import Decimal
from httpx import AsyncClient


async def test_add_dish(get_mock_menu, get_mock_submenu, ac: AsyncClient):
    response = await ac.post(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}/dishes",
        json={
            "title": "My dish 1",
            "description": "My dish 1 description",
            "price": 12.345,
        },
    )
    assert response.status_code == 201, "Блюдо не было создано"
    assert response.json()["title"] == "My dish 1"
    assert response.json()["description"] == "My dish 1 description"
    assert response.json()["price"] == '12.35'


async def test_get_dish_by_id(
    ac: AsyncClient, get_mock_menu, get_mock_submenu, get_mock_dish
):
    response = await ac.get(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}/dishes/{get_mock_dish.id}"
    )
    assert response.status_code == 200, "Такого блюда нет"
    assert response.json()["id"] == str(get_mock_dish.id)
    assert response.json()["title"] == get_mock_dish.title
    assert response.json()["description"] == get_mock_dish.description
    assert response.json()["price"] == str(Decimal(get_mock_dish.price).quantize(Decimal('0.01')))


async def test_update_dish(
    ac: AsyncClient, get_mock_menu, get_mock_submenu, get_mock_dish
):
    response = await ac.patch(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}/dishes/{get_mock_dish.id}",
        json={
            "title": "Updated Dish 1 title",
            "description": "Updated Dish 1 description",
        },
    )
    assert response.status_code == 200, "Обновление блюда не выполнено"
    assert response.json()["title"] == "Updated Dish 1 title"
    assert response.json()["description"] == "Updated Dish 1 description"
    assert response.json()["price"] == str(Decimal(get_mock_dish.price).quantize(Decimal('0.01')))


async def test_delete_dish(
    ac: AsyncClient, get_mock_menu, get_mock_submenu, get_mock_dish
):
    response = await ac.delete(
        f"/menus/{get_mock_menu.id}/submenus/{get_mock_submenu.id}/dishes/{get_mock_dish.id}"
    )
    assert response.status_code == 200, "Удаление блюда не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The dish has been deleted"
