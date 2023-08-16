from sqlalchemy import Column, String, Text

from .base import AbstractModelProject


class CharityProject(AbstractModelProject):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
