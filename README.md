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

### lazy loading relationship과 Eager loading relationship
* lazy loading

위의 User, Address 예시에서 Relationship을 설정하고 객체를 데이터베이스에 저장한 후에, 다시 해당 객체를 쿼리해서 불러올 경우 User 데이터는 가져와지지만 주소들은 SQL을 호출하지 않은 상태이다.

```
Obj = session.query(User).filter_by(name='aaa').one()

aaa	# <User('aaa', 'aaa bbb', '123456')>
```

여기서 addresses 컬랙션을 호출하는 순간 SQL이 만들어진다.

```
aaa.addresses
# [<Address(email_address='aaa@gmail.com')>]
```

이렇게 뒤늦게 SQL로 데이터를 불러오는 관계를 lazy loading relationship이라고 한다.

* Eager loading(선행 로딩) : lazt loading의 반대 개념으로 관계를 맺은 테이블을 호출할 때 바로 불러오도록 하는 방법이다. SQLAlchemy에서는 3가지 타입의 Eager loading을 사용할 수 있다.

1) Subquery Load

선행 로딩 하도록 표기하는 방법이다. orm.subqueryload() 메소드를 이용해서 서브쿼리를 불러올 때 한번에 연계해 데이터를 불러오도록 처리한다.

```
from sqlalchemy.orm import subqueryload

obj = session.query(User).options(subqueryload(User.addresses)).filter_by(name=='aaa').one()
```

2) Joined Load

또 다른 방법으로는 orm.joinedload() 메소드를 사용할 수 있다. join할 때 사용할 수 있는 방법으로 관계된 객체나 컬렉션을 한번에 불러올 수 있다.

```
from sqlalchemy.orm import joinedload

obj = session.query(User).options(joinedload(User.addresses)).filter_by(name=='aaa').one()
```

3) 명시적 Join + 선행 로딩

명시적 join이 primary 행에 위치했을 때 추가적인 테이블에 관계된 객체나 컬렉션을 불러온다.

```
from sqlalchemy.orm import contains_eager

tmpAddress = session.query(Address).join(Address.user).filter(User.name=='aaa').options(contains_eager(Address.user)).all()
```


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