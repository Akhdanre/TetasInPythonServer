from fastapi import FastAPI
from app.utils.exception_handler import ExceptionCustom, exception_400_handler
from contextlib import asynccontextmanager
from app.routes import api_router
from app.model import models
from app.database import dbConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield models.Base.metadata.create_all(bind=dbConfig.engine)


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return {"data": "selamat datang"}


app.add_exception_handler(ExceptionCustom, exception_400_handler)


app.include_router(api_router)
