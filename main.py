from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import NewUser
from database import Base

# Create the table
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for incoming request
class UserCreate(BaseModel):
    name: str
    age: int
    email: EmailStr
    mo: str

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"message": "Health is wealth!"}

@app.post("/newuser/")
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = NewUser(
        name=user.name,
        age=user.age,
        email=user.email,
        mo=user.mo
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {
        "message": "User created successfully!",
        "user_id": db_user.id,
        "name": db_user.name
    }
