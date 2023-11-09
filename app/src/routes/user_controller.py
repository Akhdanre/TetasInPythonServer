from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schema.web_response_schema import WebResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schema.register_request import RegisterRequest
from model import models

router = APIRouter()


@router.get("/api/register")
def registerController():
    return {"data": "ok"}
    # try:
    #     db_user = models.UserModel(
    #         username="ouken", password="loremipsum",
    #         name="oukenze"
    #     )
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return JSONResponse(status_code=200, content=WebResponse(data="ok").model_dump())
    # except SQLAlchemyError as e:
    #     return JSONResponse(status_code=400, content=WebResponse(errors=e).model_dump())
