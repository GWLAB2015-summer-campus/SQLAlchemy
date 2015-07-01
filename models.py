# modles.py
# python ver 2.7.3
# SQLAlchemy ver 1.0.6
# MySQL ver 5.6.25

from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(50))
    password = Column(String(20))
    def __init__(self, name ,fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    def __repr__(self):
        return "<user('%s', '%s', '%s')>" %(self.name, self.fullname, password)