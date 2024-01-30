from typing import Any
from httpx import AsyncClient
import pytest
from sqlalchemy import select

from app.main import app as fastapi_app
from app.config import settings
from app.database import Base, async_session_maker, engine

from app.menu.models import Menu
from app.submenu.models import Submenu
from app.dish.models import Dish


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session_for_test():
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def create_mock_menus():
    """
    Создание Разделов Меню для тестов.
    Первый объект Меню будет использоваться дл последующего создания Подменю и Блюд.
    Второй объект Меню будет использоваться для тестирования удаления
    """
    async with async_session_maker() as session:
        session.add_all(
            [
                Menu(title="Mock menu 1 title", description="Mock menu 1 description"),
                Menu(title="Mock menu 2 title", description="Mock menu 2 description"),
            ]
        )
        await session.commit()


@pytest.fixture(scope="session")
async def get_mock_menu(create_mock_menus) -> Menu:
    """Получение 1-го пункта меню"""
    async with async_session_maker() as session:
        stmt = select(Menu).filter_by(title="Mock menu 1 title")
        mock_menu = await session.execute(stmt)
    return mock_menu.scalar_one_or_none()


@pytest.fixture(scope="session")
async def get_mock_menu_for_test_delete(create_mock_menus) -> Menu:
    """Получение второго пункта меню"""
    async with async_session_maker() as session:
        stmt = select(Menu).filter_by(title="Mock menu 2 title")
        mock_menu_for_delete = await session.execute(stmt)
    return mock_menu_for_delete.scalar_one_or_none()


@pytest.fixture(scope="session")
async def create_mock_submenus(get_mock_menu):
    """
    Создание Разделов Подменю для тестов.
    Первый объект Подменю будет использоваться дл последующего создания Блюд.
    Второй объект Подменю будет использоваться для тестирования удаления
    """
    async with async_session_maker() as session:
        session.add_all(
            [
                Submenu(
                    title="Mock submenu 1 title",
                    description="Mock submenu 1 description",
                    menu_id=get_mock_menu.id,
                ),
                Submenu(
                    title="Mock submenu 2 title",
                    description="Mock submenu 2 description",
                    menu_id=get_mock_menu.id,
                ),
            ]
        )
        await session.commit()


@pytest.fixture(scope="session")
async def get_mock_submenu(create_mock_submenus) -> Submenu:
    """Получение первого Подменю"""
    async with async_session_maker() as session:
        stmt = select(Submenu).filter_by(title="Mock submenu 1 title")
        mock_submenu = await session.execute(stmt)
    return mock_submenu.scalar_one_or_none()


@pytest.fixture(scope="session")
async def get_mock_submenu_for_test_delete(create_mock_submenus) -> Submenu:
    """Получение второго Подменю, для тестирования удаления"""
    async with async_session_maker() as session:
        stmt = select(Submenu).filter_by(title="Mock submenu 2 title")
        mock_submenu_for_delete = await session.execute(stmt)
    return mock_submenu_for_delete.scalar_one_or_none()


@pytest.fixture(scope="session")
async def get_mock_dish(get_mock_submenu) -> Dish:
    async with async_session_maker() as session:
        mock_dish = Dish(
            title="Mock dish 1 title",
            description="Mock dish 1 description",
            price=15.99,
            submenu_id=get_mock_submenu.id,
        )
        session.add(mock_dish)
        await session.commit()
        await session.refresh(mock_dish)
        return mock_dish


@pytest.fixture(scope="module")
async def save_data() -> dict[str, Any]:
    """Фикстура для сохранения данных в интеграционных тестах"""
    return {}