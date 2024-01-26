from httpx import AsyncClient

menu_id = None


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

    # Записываем значение в глобальную переменную, для обращения к созданному меню по UUID
    global menu_id
    menu_id = response.json()["id"]


async def test_get_menu_by_id(ac: AsyncClient):
    response = await ac.get(f"/menus/{menu_id}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == "Menu 1 title"
    assert response.json()["description"] == "Menu 1 description"


async def test_update_menu(ac: AsyncClient):
    response = await ac.patch(
        f"/menus/{menu_id}",
        json={
            "title": "Updated Menu 1 title",
            "description": "Updated Menu 1 description",
        },
    )
    assert response.status_code == 200, "Обновление меню не выполнено"
    assert response.json()["id"] == menu_id
    assert response.json()["title"] == "Updated Menu 1 title"
    assert response.json()["description"] == "Updated Menu 1 description"


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/menus/{menu_id}")
    assert response.status_code == 200, "Удаление меню не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The menu has been deleted"
