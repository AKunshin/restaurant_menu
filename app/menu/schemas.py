from pydantic import UUID4, BaseModel


class SMenuBase(BaseModel):
    id: UUID4


class SMenuCreate(SMenuBase):
    title: str
    description: str


class SMenus(SMenuCreate):
    submenus_count: int = 0
    dishes_count: int = 0
