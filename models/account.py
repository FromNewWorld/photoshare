from sqlalchemy import (Column,Integer,String,DateTime)
from datetime import datetime
from sqlalchemy.sql import exists

from .db import Base,DBSession

session = DBSession()
class User(Base):
    __tablename__='users'

    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    created = Column(DateTime,default=datetime.now)
    email = Column(String(50))
    last_login = Column(DateTime)

    @classmethod
    def exists_it(cls,username):
        '''

        :param username: 用户名
        :return: 返回是否该用户名的数据存在（True/False）
        '''
        return session.query(exists().where(User.name == username)).scalar()

    @classmethod
    def get_password(cls,username):
        '''
            获取password，若没有password则返回空（‘’）
        '''
        user = session.query(cls).filter_by(name=username).first() #获取name=username的那一条数据
        if user:
            return user.password
        else:
            return ''

    @classmethod
    def add_user(cls,username,password,email=''):
        '''
        增加一条数据到数据表中
        :param username: 用户名
        :param password: 用户密码
        :param email: 邮箱
        '''
        user=User(name=username,password=password,email=email,last_login = datetime.now())
        session.add(user)
        session.commit()


    def update_last_login(username):
        """
        更新上次登入的时间
        """
        t = datetime.now()
        session.query(User).filter_by(name=username).update({User.last_login:t})
        session.commit()


    def __repr__(self):
        return '< User({}:{}) >'.format(self.id,self.name)


if __name__=='__main__':
    Base.metadata.create_all()
