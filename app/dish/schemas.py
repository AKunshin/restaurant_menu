from pydantic import UUID4, BaseModel, ConfigDict, field_validator
from decimal import Decimal


class SDishBase(BaseModel):
    title: str
    description: str
    price: Decimal

    @field_validator("price", mode="before")
    @classmethod
    def round_for_two_digits(cls, v):
        """Округление цены до 2-ух цифр после разделителя"""
        return Decimal(v).quantize(Decimal("1.00"))


class SDishCreate(SDishBase):
    pass


class SDishUpdate(SDishCreate):
    pass


class SDishUpdatePartial(SDishCreate):
    title: str | None = None
    description: str | None = None
    price: Decimal | None = None

    @field_validator("price", mode="before")
    @classmethod
    def round_for_two_digits(cls, v):
        return Decimal(v).quantize(Decimal("1.00"))


class SDish(SDishBase):
    id: UUID4

    model_config = ConfigDict(from_attributes=True)
