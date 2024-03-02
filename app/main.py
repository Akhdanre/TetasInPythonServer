from fastapi import FastAPI
from utils.exception_handler import ExceptionCustom, exception_400_handler
from contextlib import asynccontextmanager
from routes import api_router
from model import models
from database import dbConfig
from uvicorn import run
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield models.Base.metadata.create_all(bind=dbConfig.engine)


app = FastAPI(lifespan=lifespan)

# app.add_middleware(HTTPSRedirectMiddleware)


@app.get("/")
def home():
    return {"data": "selamat datang"}


app.add_exception_handler(ExceptionCustom, exception_400_handler)


app.include_router(api_router)


if __name__ == "__main__":
    # run(app, host="0.0.0.0", port=443,
    #     ssl_keyfile="key.pem", ssl_certfile="cert.pem")
    run(app, host="0.0.0.0", port=8000, reload=True)
