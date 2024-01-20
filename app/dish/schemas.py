from pydantic import UUID4, BaseModel, validator
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


class SDish(SDishBase):
    id: UUID4
