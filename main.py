# main.py
# python ver 2.7.3
# SQLAlchemy ver 1.0.6
# MySQL ver 5.6.25

from database import init_db
from database import db_session
from models import User, Address
import query

def main():
    # insert User
    print 'Insert Example\n'
    user1 = User('junki', 'Junki Kim', '12345')
    user2 = User('aaa', 'aaaa bb', '654321')
    query.insertUser(user1)
    query.insertUser(user2)
    
    # show table
    print "\n\n Show tables\n"
    query.show_tables()

    # select user
    print 'Select Example\n'
    query.selectUser(user1)

    # delete user
    print 'Delete Example\n'
    query.deleteUser(user2)
    print "\n\n Show tabales\n"
    query.show_tables()

    # update user
    print 'Update Example\n'
    updateuser = User('junki', 'Junki Kim', '654321')
    query.updateUser(user1, updateuser)
    query.show_tables()

    # Usage relationship
    print 'Relationship Example\n'
    print "Create tmpUser('aaa', 'bbb aaa', '12345678')\n"
    tmpUser = User('aaa', 'bbb aaa', '12345678')
    print "tmpUser's email address\n"
    tmpUser.addresses

    print 'Add email address\n'
    tmpUser.addresses = [Address(email_address='aaa@gmail.com'), Address(email_address='aaa@naver.com')]
    tmpUser.addresses

    print 'Insert tmpUser'
    query.insertUser(tmpUser)

    print 'Select tmpUser'
    query.selectUser(tmpUser)

if __name__=="__main__":
    main()