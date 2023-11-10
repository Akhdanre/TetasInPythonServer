from app.database.dbConfig import session_scope
from app.schema.web_response_schema import WebResponse
from app.schema.register_request import RegisterRequest
from app.model import models
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .validation_service import ValidationService
from fastapi import HTTPException, status
from passlib.context import CryptContext


class User:
    def register(user: RegisterRequest, db: Session):
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
            pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
            hashPassword = pwd_context.hash(user.password)
            db_user = models.UserModel(
                username=user.username,
                password=hashPassword,
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

    def deleteAllUsers():
        """delete all users data for testing, table must null for check"""
        with session_scope() as db:
            db_user_count = db.query(models.UserModel).delete()
            if db_user_count > 0:
                db.commit()
                return True
            return False
