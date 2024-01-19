from fastapi import FastAPI

from app.menu.router import router as router_menus
from app.submenu.router import router as router_submenu
from app.dish.router import router as router_dish

app = FastAPI(root_path="/api/v1")

app.include_router(router_menus)
app.include_router(router_submenu)
app.include_router(router_dish)
