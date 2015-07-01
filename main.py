# main.py
# python ver 2.7.3
# SQLAlchemy ver 1.0.6
# MySQL ver 5.6.25

from database import init_db
from database import db_session
from models import User

# Add Query
def insertUser(name, fullname, password):
    tmpUser = User(name, fullname, password)
    db_session.add(tmpUser)
    db_session.commit()

# Delete Query
def deleteUser(name, fullname, password):
    db_session.query(User).filter_by(name = name, fullname = fullname, password = password).delete()
    db_session.commit()

# Update Query
def updateUser(name, fullname, password, pname, pfullname, ppassword):
    db_session.query(User).filter_by(name = name, fullname = fullname, password = password).update({"name" : pname, "fullname" : pfullname, "password" : ppassword})
    db_session.commit()

# Select Query
def selectUser(name, fullname, password):
    tmpUser = db_session.query(User).filter_by(name = name, fullname = fullname, password = password)
    print tmpUser

# Show table
def show_tables():
    queries = db_session.query(User)
    entires = [dict(id=q.id, name=q.name, fullname=q.fullname, password=q.password) for q in queries]

    print entires

def main():
    # insert User
    insertUser('junki', 'Junki Kim', '123456')
    insertUser('aaa', 'aaaa bb', '654321')
    
    # show table
    print "\n\n Show tables\n"
    show_tables()

    # select user
    selectUser('junki', 'Junki Kim', '123456')

    # delete user
    deleteUser('aaa', 'aaaa bb', '654321')
    print "\n\n Show tabales\n"
    show_tables()

    # update user
    updateUser('junki', 'Junki Kim', '123456', 'junki', 'Junki Kim', '654321')
    show_tables()

if __name__=="__main__":
    main()
