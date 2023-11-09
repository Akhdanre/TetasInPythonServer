from fastapi import FastAPI
import uvicorn
from app.routes import api_router
from app.model import models
from app.database import dbConfig
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield models.Base.metadata.create_all(bind=dbConfig.engine)


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

