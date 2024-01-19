from pydantic import UUID4, BaseModel


class SSubmenuBase(BaseModel):
    id: UUID4


class SSubmenuCreate(SSubmenuBase):
    title: str
    description: str


class SSubmenus(SSubmenuCreate):
    dishes_count: int = 0
