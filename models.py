from sqlalchemy import Column, Integer, String
from database import Base

class NewUser(Base):
    __tablename__ = "newuser"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String, unique=True)
    mo = Column(String)
