from datetime import datetime
from typing import Optional

from pydantic import Extra, PositiveInt
from .base import General_Scheme


class DonationBase(General_Scheme):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    comment: Optional[str]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True