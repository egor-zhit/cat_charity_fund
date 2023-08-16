from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class General_Scheme(BaseModel):
    full_amount: Optional[PositiveInt]
    invested_amount: Optional[int] = 0
    fully_invested: Optional[bool] = False
    create_date: Optional[datetime]
    close_date: Optional[datetime]