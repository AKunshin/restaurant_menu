from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base
from app.submenu.models import Submenu


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))

    menu = relationship("Submenu", back_populates="dishes")