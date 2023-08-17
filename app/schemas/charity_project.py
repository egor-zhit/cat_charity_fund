from typing import Optional

from pydantic import Field, PositiveInt, validator
from .base import General_Scheme


ERROR_MESSAGE = 'Данную строку нельзя редактировать'


class ProjectBase(General_Scheme):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)

    @validator('name')
    def name_not_empty(cls, value: str):
        if not value:
            raise ValueError('Не может быть пустым')
        return value

    @validator('description')
    def description_not_empty(cls, value: str):
        if not value:
            raise ValueError('Не может быть пустым')
        return value


class ProjectCreate(ProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class ProjectUpdate(ProjectBase):

    @validator('fully_invested')
    def fully_invested(cls, value: bool):
        if value is True:
            raise ValueError('Закрытый проект нельзя редактировать')
        return value

    @validator('invested_amount')
    def invested_amount(cls, value: bool):
        if value:
            raise ValueError(ERROR_MESSAGE)
        return value

    @validator('create_date')
    def create_date(cls, value: bool):
        if value:
            raise ValueError(ERROR_MESSAGE)
        return value

    @validator('close_date')
    def close_date(cls, value: bool):
        if value:
            raise ValueError(ERROR_MESSAGE)
        return value


class ProjectDB(ProjectBase):
    id: int

    class Config:
        orm_mode = True
