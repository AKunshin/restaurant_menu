from sqlalchemy import Column, String, UUID, func, select
from sqlalchemy.orm import relationship, column_property

from app.database import Base
from app.submenu.models import Submenu


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submenus_count = column_property(
        select(func.count(Submenu.id)).where(Submenu.menu_id == id).scalar_subquery()
    )
    dishes_count = column_property(select(Submenu.dishes_count))

    submenus = relationship("Submenu", back_populates="menu")
