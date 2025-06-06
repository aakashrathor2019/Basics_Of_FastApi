from sqlalchemy import Column, Integer, String
from database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional


class NewUser(Base):
    __tablename__ = "newuser"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    mo = Column(String)



class UserPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    mo: Optional[str] = None
