# coding: utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String,create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)
    param1 = Column(String(50))
    param2 = Column(String(50))


class Student(Base):
    __tablename__ = 'student'

    def __init__(self, sname, sno, sphone, semail):
        self.sname = sname
        self.sno = sno
        self.sphone = sphone
        self.semail = semail

    id = Column(Integer, primary_key=True)
    sname = Column(String(20), nullable=False)
    sno = Column(String(20), nullable=False)
    sphone = Column(String(20), nullable=False)
    semail = Column(String(50), nullable=False)
    param1 = Column(String(50))
    param2 = Column(String(50))
    param3 = Column(String(50))

engine = create_engine('mysql+mysqlconnector://root:563255387@127.0.0.1:3306/studentmanagersystem')

DBSession = sessionmaker(bind = engine)
