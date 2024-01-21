import uuid
from sqlalchemy import UUID, Column, ForeignKey, String, select, func
from sqlalchemy.orm import relationship, column_property

from app.database import Base
from app.dish.models import Dish


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID, default=uuid.uuid4, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    dishes_count = column_property(
        select(func.count(Dish.id)).where(Dish.submenu_id == id).scalar_subquery()
    )
    menu_id = Column(UUID, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu")
