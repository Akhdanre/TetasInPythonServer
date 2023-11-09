from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager


from app.routes import api_router
from app.model import models
from app.database import dbConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield models.Base.metadata.create_all(bind=dbConfig.engine)


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)



