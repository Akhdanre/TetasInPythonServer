from fastapi import FastAPI
import uvicorn
from routes import api_router
from model import models
from database import dbConfig
from contextlib import asynccontextmanager

app = FastAPI()

app.include_router(api_router)

@asynccontextmanager
async def lifespan(app: app):
    models.Base.metadata.create_all(bind=dbConfig.engine)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
