from pydantic import UUID4, BaseModel


class SSubmenuBase(BaseModel):
    title: str
    description: str


class SSubmenuCreate(SSubmenuBase):
    pass


class SSubmenus(SSubmenuCreate):
    id: UUID4
    dishes_count: int = 0
