import uuid
from sqlalchemy import Column, String, func, select, UUID
from sqlalchemy.orm import relationship, column_property

from app.database import Base
from app.dish.models import Dish
from app.submenu.models import Submenu


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, default=uuid.uuid4, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = column_property(
        select(func.count(Submenu.id)).where(Submenu.menu_id == id).correlate_except(Submenu).scalar_subquery()
    )
    dishes_count = column_property(select(Submenu.dishes_count).correlate_except(Dish).scalar_subquery())

    submenus = relationship("Submenu", cascade="all, delete-orphan", back_populates="menu")
