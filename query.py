# query.py

from models import User, Address
from database import db_session
from database import init_db

# Add Query
def insertUser(user):
    db_session.add(user)
    db_session.commit()

# Delete Query
def deleteUser(user):
    db_session.query(User).filter_by(name = user.name, fullname = user.fullname, password = user.password).delete()
    db_session.commit()

# Update Query
def updateUser(source, update):
    db_session.query(User).filter_by(name = source.name, fullname = source.fullname, password = source.password).update({"name" : update.name, "fullname" : update.fullname, "password" : update.password})
    db_session.commit()

# Select Query
def selectUser(user):
    tmpUser = db_session.query(User).filter_by(name = user.name, fullname = user.fullname, password = user.password)
    print tmpUser

# Show table
def show_tables():
    queries = db_session.query(User)
    entires = [dict(id=q.id, name=q.name, fullname=q.fullname, password=q.password) for q in queries]
    print entires