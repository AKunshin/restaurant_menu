import asyncio
import json
import pytest
from sqlalchemy import insert

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

    def open_mock_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    menus = open_mock_json("menus")

    # submenus = open_mock_json("submenus")
    # dishes = open_mock_json("dishes")


    async with async_session_maker() as session:
        add_menus = insert(Menu).values(menus)

        # add_submenus = insert(Submenu).values(submenus)
        # add_dishes = insert(Dish).values(dishes)

        await session.execute(add_menus)

        # await session.execute(add_submenus)
        # await session.execute(add_dishes)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()