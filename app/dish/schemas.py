from pydantic import UUID4, BaseModel, ConfigDict, validator
from decimal import Decimal


class SDishBase(BaseModel):
    title: str
    description: str
    price: Decimal

    @validator("price", pre=True)
    def round_for_two_digits(cls, v):
        return Decimal(v).quantize(Decimal("1.00"))


class SDishCreate(SDishBase):
    pass


class SDishUpdate(SDishCreate):
    pass


class SDishUpdatePartial(SDishCreate):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None

    @validator("price", pre=True)
    def round_for_two_digits(cls, v):
        return Decimal(v).quantize(Decimal("1.00"))


class SDish(SDishBase):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)
