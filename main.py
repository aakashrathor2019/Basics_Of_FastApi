from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import NewUser, UserPatch
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

@app.get("/newuser/")
def read_all_users(db: Session = Depends(get_db)):
    users = db.query(NewUser).all()
    return users

@app.get("/newuser/{user_id}")
def read_any_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(NewUser).filter(NewUser.id == user_id).first()
    if user:
        return user
    return {"message": "No user found with this Id!"}

@app.put("/newuser/{user_id}")
def update_user(user_id: int, user:UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(NewUser).filter(NewUser.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.age = user.age
        db_user.email = user.email
        db_user.mo = user.mo
        db.commit()
        db.refresh(db_user)
        return {"message": "Record updated successfully!"}
    return {"message":" record not found!"}

@app.patch("/newuser/{user_id}")
def partial_update_user(user_id: int, user:UserPatch, db:Session = Depends(get_db)):
    print("Patch method called")
    db_user = db.query(NewUser).filter(NewUser.id == user_id).first()
    print("User found:", db_user)
    print("User data:", user)
    if db_user:
        print(user)
        if user.name:
            db_user.name = user.name
        if user.age > 0:
            db_user.age = user.age
        if user.email:
            db_user.email = user.email
        if user.mo:
            db_user.mo = user.mo
        db.commit()
        db.refresh(db_user)
        return {"messge":"Partial update done"}
    return {"message":" There is no record with this id!"}

@app.delete("/newuser/{user_id}")
def delete_user(user_id:int, db: Session = Depends(get_db)):
    db_user = db.query(NewUser).filter(NewUser.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {"message": "Record deleted successfully!"}
    return {"message": "Record not found"}


