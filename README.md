# Python에서 SQLAlchemy 사용 예시

## 구현 환경
* Python : 2.7.3
* SQLAlchemy : 1.0.6
* MySQL 5.6.25

## 파일 설명
database.py : MySQL Server와 연결을 생성하고 SQLAlchemy를 사용하기 위한 Session을 생성하는 코드

models.py : RDBMS의 테이블의 각 속성들을 매핑할 예제 클래스가 선언된 코드

main.py : SQLAlchemy를 사용해서 데이터베이스에 있는 데이터를 생성/수정/삭제하는 쿼리가 구현되어 있는 코드

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