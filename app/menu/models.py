from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(UUID, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    submenus = relationship("Submenu", back_populates="menu")