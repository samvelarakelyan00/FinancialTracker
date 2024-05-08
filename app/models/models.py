from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Operation(Base):
    __tablename__ = "operations"

    operation_id = Column(Integer, nullable=False, primary_key=True)
    date = Column(Date, nullable=False)
    kind = Column(String, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
