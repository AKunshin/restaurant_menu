from httpx import AsyncClient


target_submenu_id = None


async def test_add_submenu(ac: AsyncClient):
    response = await ac.post(
        f"/{target_menu_id}/submenus",
        json={
            "title": "Submenu 1 title",
            "description": "Submenu 1 description",
        },
    )
    print(f"{target_menu_id=}")
    assert response.status_code == 201, "Подменю не было создано"
    assert "id" in response.json()
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"


async def test_get_submenu_by_id(ac: AsyncClient):
    response = await ac.get(f"/{target_menu_id}/submenus/{target_submenu_id}")
    assert response.status_code == 200, "Такого меню нет"
    assert response.json()["id"] == target_submenu_id
    assert response.json()["title"] == "Submenu 1 title"
    assert response.json()["description"] == "Submenu 1 description"


async def test_update_menu(ac: AsyncClient):
    response = await ac.patch(
        f"/{target_menu_id}/submenus/{target_submenu_id}",
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
    response = await ac.delete(f"/{target_menu_id}/submenus/{target_submenu_id}")
    assert response.status_code == 200, "Удаление подменю не выполнено"
    assert response.json()["status"] == "true"
    assert response.json()["message"] == "The submenu has been deleted"
