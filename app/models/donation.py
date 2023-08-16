from sqlalchemy import Column, Text, Integer, ForeignKey

from .base import AbstractModelProject


class Donations(AbstractModelProject):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
