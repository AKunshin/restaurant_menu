from pydantic import UUID4, BaseModel, ConfigDict


class SMenuBase(BaseModel):
    title: str
    description: str


class SMenuCreate(SMenuBase):
    pass


class SMenuUpdate(SMenuCreate):
    pass


class SMenuUpdatePartial(SMenuCreate):
    title: str | None = None
    description: str | None = None


class SMenu(SMenuBase):
    id: UUID4
    submenus_count: int  = 0
    dishes_count: int  = 0

    model_config = ConfigDict(from_attributes=True)
