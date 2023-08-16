from sqlalchemy import Column, Text, Integer, ForeignKey

from .base import AbstractModelProject


class Donation(AbstractModelProject):
    comment = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'))
