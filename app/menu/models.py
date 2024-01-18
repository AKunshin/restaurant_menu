from sqlalchemy import Column, Integer, String
from app.database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)