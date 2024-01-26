import asyncio
from typing import Any
from httpx import AsyncClient
import pytest

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
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def session_for_test():
    async with async_session_maker() as session:
        yield session


# Remove if unuse
@pytest.fixture(scope="module")
async def save_data() -> dict[str, Any]:
    data = {}
    return data


@pytest.fixture(scope="module")
async def get_mock_menu() -> Menu:
    async with async_session_maker() as session:
        mock_menu = Menu(
            title="Mock menu 1 title", description="Mock menu 1 description"
        )
        await session.execute(mock_menu)
        await session.commit()
        await session.refresh(mock_menu)
        return mock_menu


@pytest.fixture(scope="module")
async def get_mock_submenu(get_mock_menu) -> Submenu:
    async with async_session_maker() as session:
        mock_submenu = Submenu(
            title="Mock submenu 1 title",
            description="Mock submenu 1 description",
            menu_id=get_mock_menu.id,
        )
        await session.execute(mock_submenu)
        await session.commit()
        await session.refresh(mock_submenu)
        return mock_submenu


@pytest.fixture(scope="module")
async def get_dish_submenu(get_mock_submenu) -> Dish:
    async with async_session_maker() as session:
        mock_dish = Dish(
            title="Mock dish 1 title",
            description="Mock dish 1 description",
            price=15.99,
            submenu_id=get_mock_submenu.id,
        )
        await session.execute(mock_dish)
        await session.commit()
        await session.refresh(mock_dish)
        return mock_dish
