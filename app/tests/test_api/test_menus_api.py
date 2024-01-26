from httpx import AsyncClient


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


async def test_get_menu_by_id(ac: AsyncClient, get_mock_menu):
    response = await ac.get(f"/menus/{get_mock_menu.id}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == get_mock_menu.id
    assert response.json()["title"] == get_mock_menu.title
    assert response.json()["description"] == get_mock_menu.description


async def test_update_menu(ac: AsyncClient, get_mock_menu):
    response = await ac.patch(
        f"/menus/{get_mock_menu.id}",
        json={
            "title": "Updated mock menu 1 title",
            "description": "Updated mock menu 1 description",
        },
    )
    assert response.status_code == 200, "Обновление меню не выполнено"
    assert response.json()["id"] == get_mock_menu.id
    assert response.json()["title"] == "Updated mock menu 1 title"
    assert response.json()["description"] == "Updated mock menu 1 description"


async def test_delete_menu(ac: AsyncClient, get_mock_menu):
    response = await ac.delete(f"/menus/{get_mock_menu.id}")
    assert response.status_code == 200, "Удаление меню не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The menu has been deleted"
