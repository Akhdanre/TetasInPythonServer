from fastapi import FastAPI
import uvicorn
from routes import api_router
from model import models
from database import dbConfig
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield models.Base.metadata.create_all(bind=dbConfig.engine)


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)

