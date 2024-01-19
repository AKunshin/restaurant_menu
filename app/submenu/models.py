from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(UUID, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    menu_id = Column(UUID, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")