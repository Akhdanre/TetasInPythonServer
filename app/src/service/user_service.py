from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model import models
from schema.register_request import RegisterRequest
from schema.web_response_schema import WebResponse
from .validation_service import ValidationService
from fastapi import HTTPException, status
import json


class User:
    def register(user: RegisterRequest, db: Session):
        if ValidationService.validation(user.username, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already exist"
            )
        try:
            db_user = models.UserModel(
                username=user.username,
                password=user.password,
                name=user.name
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return WebResponse(data="ok")
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
