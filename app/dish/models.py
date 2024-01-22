import uuid
from sqlalchemy import DECIMAL, UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(UUID, default=uuid.uuid4, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    submenu_id = Column(UUID, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")