from app.database.dbConfig import session_scope
import app.schema as schema
from app.model import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .validation_service import ValidationService
from fastapi import HTTPException, status
from app.utils import get_password_context, ExceptionCustom, WebResponseData


class User:
    def register(user: schema.RegisterRequest, db: Session):
        if user.username == "" or user.password == "" or user.name == "":
            raise ExceptionCustom(
                status_code=400, detail="field can't blank!!!")
        if ValidationService.validation(user.username, db):
            raise ExceptionCustom(
                status_code=400, detail="username already exist")
        try:
            hashPassword = get_password_context().hash(user.password)
            db_user = models.UserModel(
                username=user.username,
                password=hashPassword,
                name=user.name
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return WebResponseData(data="ok")
        except SQLAlchemyError as e:
            raise ExceptionCustom(
                status_code=500, detail=str(e))

    def updateUsers(user: schema.UserUpdateRequest, apiToken: str, db: Session):
        exist_user = db.query(models.UserModel).filter_by(
            token=apiToken).first()
        if exist_user:
            try:
                exist_user.password = get_password_context().hash(user.password)
                exist_user.name = user.name

                db.commit()
                db.refresh(exist_user)
            except SQLAlchemyError as e:
                raise ExceptionCustom(
                    status_code=500, detail=str(e))

    def deleteAllUsers():
        """delete all users data for testing, table must null for check"""
        with session_scope() as db:
            db_user_count = db.query(models.UserModel).delete()
            if db_user_count > 0:
                db.commit()
                return True
            return False
