__author__ = 'wei'
from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime
class Tweet(Base):
    __tablename__ = 'TwitterMap'
    id = Column(String(120), primary_key=True)
    text = Column(String(140))
    geo = Column(String(120))
    author_name = Column(String(120))
    author_id = Column(String(120))
    author_url = Column(String(140))
    date = Column(String(140))

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return self.id

