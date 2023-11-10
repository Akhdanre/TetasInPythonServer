from app.database.dbConfig import session_scope
import app.schema as schema
from app.model import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .validation_service import ValidationService
from fastapi import HTTPException, status
from uuid import uuid4
from app.utils.deps import get_password_context


class User:
    def register(user: schema.RegisterRequest, db: Session):
        if user.username == "" and user.password == "" and user.name == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fields must not be blank"
            )
        if ValidationService.validation(user.username, db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="username already exist"
            )
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
            return schema.WebResponse(data="ok")
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def updateUsers(user: schema.UserUpdateRequest, apiToken: str, db: Session):
        exist_user = db.query(models.UserModel).filter_by(token=apiToken).first()
        if exist_user:
            try:
                exist_user.password = get_password_context().hash(user.password)
                exist_user.name = user.name

                db.commit()
                db.refresh(exist_user)
            except SQLAlchemyError as e:
                raise HTTPException

    def deleteAllUsers():
        """delete all users data for testing, table must null for check"""
        with session_scope() as db:
            db_user_count = db.query(models.UserModel).delete()
            if db_user_count > 0:
                db.commit()
                return True
            return False

    