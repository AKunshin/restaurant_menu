from pydantic import UUID4, BaseModel, ConfigDict


class SSubmenuBase(BaseModel):
    title: str
    description: str


class SSubmenuCreate(SSubmenuBase):
    pass


class SSubmmenuUpdate(SSubmenuCreate):
    pass


class SSubmmenuUpdatePartial(SSubmenuCreate):
    title: str | None = None
    description: str | None = None


class SSubmenu(SSubmenuCreate):
    id: UUID4
    dishes_count: int = 0

    model_config = ConfigDict(from_attributes=True)
