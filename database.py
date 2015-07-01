# database.py
# python ver 2.7.3
# SQLAlchemy ver 1.0.6
# MySQL ver 5.6.25

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create SQLAlchemy engine
engine = create_engine('mysql://root:123456@localhost/SQLAlchemyTest?charset=utf8', convert_unicode=False, echo=True)

# Mapping declare
# Create class and Connect real DB table
Base = declarative_base()

# Create Session
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db():
    import models
    Base.metadata.create_all(engine)