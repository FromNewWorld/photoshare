from sqlalchemy import (Column,Integer,String,DateTime)
from datetime import datetime

from .db import Base

class User(Base):
    __tablename__='users'


    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50),unique=True,nullable=False)
    password = Column(String(50),nullable=False)
    # created = Column(DateTime,default=datetime.now)
    # last_login = Column(DateTime)


    def __repr__(self):
        return '< User({}:{}) >'.format(self.id,self.name)


if __name__=='__main__':
    Base.metadata.create_all()
