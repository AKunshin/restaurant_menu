from pydantic import UUID4, BaseModel


class SMenuBase(BaseModel):
    title: str
    description: str

class SMenuCreate(SMenuBase):
    pass


class SMenus(SMenuCreate):
    id: UUID4
    submenus_count: int = 0
    dishes_count: int = 0
