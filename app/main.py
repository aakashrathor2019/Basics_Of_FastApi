from fastapi import FastAPI
from app.models.database import engine, Base
from app.routers.routings import router 

# Create the table
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"message": "Health is wealth!"}

app.include_router(router)