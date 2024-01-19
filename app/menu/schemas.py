from pydantic import UUID4, BaseModel


class SMenuBase(BaseModel):
    pass

class SMenuCreate(SMenuBase):
    title: str
    description: str


class SMenus(SMenuCreate):
    id: UUID4
    submenus_count: int = 0
    dishes_count: int = 0
