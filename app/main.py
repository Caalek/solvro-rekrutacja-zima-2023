from fastapi import FastAPI
from . import models
from .database import SessionLocal, engine
from .routers import developer, project
from dotenv import load_dotenv

load_dotenv()
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(developer.router)
app.include_router(project.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
