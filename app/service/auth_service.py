import app.schema as schema
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.model import models
from uuid import uuid4
from app.utils.deps import get_password_context


class Authetication:
    def login(userReq: schema.AuthRequest, db: Session):
        try:
            user = db.query(models.UserModel).filter_by(
                username=userReq.username).first()
            is_pass_true = get_password_context().verify(userReq.password, user.password)
            if user is not None and is_pass_true:
                user.token = uuid4()
                db.commit()
                db.refresh(user)
                return schema.WebResponse(data={
                    "token": user.token
                })
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "errors": "user unauthorized"
                }
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": e}
            )

    def logout(token: str, db: Session):
        try:
            user = db.query(models.UserModel).filter_by(
                token=token).first()
            if user is not None:
                user.token = None
                db.commit()
                db.refresh(user)
                return schema.WebResponse(data="ok")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "errors": "user unauthorized"
                }
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"errors": e}
            )
