from httpx import AsyncClient

target_menu_id = None
target_submenu_id = None

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
    assert "id" in response.json()
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"
    global target_submenu_id
    target_submenu_id = response.json()["id"]


async def test_get_submenu_by_id(ac: AsyncClient):
    response = await ac.get(
        f"/menus/{target_menu_id}/submenus/{target_submenu_id}"
    )
    assert response.status_code == 200, "Такого подменю нет"
    assert response.json()["id"] == target_submenu_id
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"


async def test_update_menu(ac: AsyncClient):
    response = await ac.patch(
        f"/menus/{target_menu_id}/submenus/{target_submenu_id}",
        json={
            "title": "Updated Submenu 1 title",
            "description": "Updated Submenu 1 description",
        },
    )
    assert response.status_code == 200, "Обновление подменю не выполнено"
    assert response.json()["id"] == target_submenu_id
    assert response.json()["title"] == "Updated Submenu 1 title"
    assert response.json()["description"] == "Updated Submenu 1 description"


async def test_delete_menu(ac: AsyncClient):
    response = await ac.delete(f"/menus/{target_menu_id}/submenus/{target_submenu_id}")
    assert response.status_code == 200, "Удаление подменю не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The submenu has been deleted"
