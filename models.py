# modles.py
# python ver 2.7.3
# SQLAlchemy ver 1.0.6
# MySQL ver 5.6.25

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    fullname = Column(String(50))
    password = Column(String(20))
    addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")
    def __init__(self, name ,fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password
    def __repr__(self):
        return "<user('%s', '%s', '%s')>" %(self.name, self.fullname, self.password)

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    def __init__(self, email_address):
        self.email_address = email_address
    def __repr__(self):
        return "<Address('%s')>" % self.email_address

