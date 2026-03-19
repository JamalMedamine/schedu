from sqlalchemy import Column, Integer, String
from utils.db import Base

class User(Base):
    __tablename__ = "users"

    id    = Column(Integer, primary_key=True, index=True)
    firstName  = Column(String, nullable=False)
    lastName  = Column(String, nullable=False)
    email = Column(String, nullable=False,unique=True)
    password =  Column(String, nullable=False)