"""
    create by Gray 2019-05-29
"""
from sqlalchemy import Column, Integer, SmallInteger, String

from ArticleSpider.models.base import Base


class Newrank(Base):
    title = Column(String(50), nullable=False)
    url = Column(String(50), nullable=False, primary_key=True, autoincrement=False)
