# Python에서 SQLAlchemy 사용하기

## 구현 환경
* Python : 2.7.3
* SQLAlchemy : 1.0.6
* MySQL 5.6.25

## 파일 설명
* database.py : MySQL Server와 연결을 생성하고 SQLAlchemy를 사용하기 위한 Session을 생성하는 파일

* models.py : RDBMS의 테이블의 각 속성들을 매핑할 예제 클래스가 선언된 파일

* query.py : 테스트 케이스에서 사용할 쿼리가 구현되어 있는 파일

* main.py : 테스트 케이스

## 쿼리 종류 및 구현
#### Insert
```
session.add('추가할 객체 이름')
session.commit()

ex) User를 DB에 추가
	tmpUser = User(name, fullname, password)
	session.add(tmpUser)
	session.commit()
```

#### Delete
```
session.query('삭제할 객체 타입').filter_by('삭제할 객체 정보')
session.commit()

ex) 입력한 name, fullname, password가 모두 일치하는 User 삭제
	session.query(User).filter_by(name=name, fullname=fullname, password=password).delete()
    session.commit()
```

####  Update
```
session.query('수정할 객체 타입').filter_by('수정할 객체 정보').update('수정 사항')
session.commit()

ex) 입력한 name, fullname, password가 모두 일치하는 User의 정보 수정
	session.query(User).filter_by(name = name, fullname = fullname, password = password).update({"name" : pname, "fullname" : pfullname, "password" : ppassword})
    session.commit()
```

#### Select
```
Obj = session.query('검색할 객체 타입').filter_by('검색 옵션')

ex) 입력한 name, fullname, password가 모두 일치하는 User 검색
	tmpUser = session.query(User).filter_by(name = name, fullname = fullname, password = password)
    print tmpUser
```

## 관계(Relationship) 만들기
```
예제 코드에 Address 객체를 추가하고 User 객체를 아래와 같이 수정한다.

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", backref='user', cascade="all, delete, delete-orphan")
    def __repr__(self):
        return "<User('%s','%s','%s'>" % (self.name, self.fullname, self.password)
```
* relationship() 함수를 호출하여 Address 클래스가 User 클래스에 연결되어 있다고 선언한다.
* 여기서 cascade 설정을 하지 않으면 User가 삭제되어도 Address가 남아 있기 때문에 문제가 발생한다.

```
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    def __repr__(self):
        return "<Address('%s')>" % self.email_address

```
* Foreign Key를 추가하여 Address 테이블과 User 테이블의 관계를 설정한다.

## JOIN 사용하기
* 단순히 완전 조인을 사용한다면 filter() 메소드를 이용해 Join할 수 있다.

```
session.query(User, Address).filter(User.id == Address.user_id).filter(Address.email_address == 'aaa@gmail.com').all()
```

* 실제 SQL에서 사용하는 Join 문법을 사용하려면 Query.join() 메소드를 사용한다.

```
session.query(User).join(Address).filter(Address.email_address=='aaa@gmail.com').all()
```
이 때 User와 Address 사이에 있는 하나의 외래키를 기준으로 join한다.

* 외부 join은 outerjoin() 메소드를 사용한다.

```
seession.query.outerjoin(User.addresses)	# left outer join
```

## 서브쿼리 사용하기
```
subq = session.query(Address.user_id, func.count('*').label('address_count')).group_by(Address.user_id).subquery()
```

* 위의 코드를 보면 서브 쿼리로 사용할 쿼리를 작성한 후 .subquery() 메소드를 사용하는데, subquery() 메소드는 별칭을 이용해 다른 query에 포함할 수 있는 SELECT 명령문의 형태로 쿼리를 반환해준다.