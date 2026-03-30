from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from utils.db import Base

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    firstName : Mapped[str] = mapped_column(String, nullable=False)
    lastName : Mapped[str] = mapped_column(String, nullable=False)
    email : Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String, nullable=False)