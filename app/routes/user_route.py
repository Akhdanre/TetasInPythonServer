from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from utils.deps import get_db
import schema as schema
from service.user_service import User
from typing import Annotated, Union


router = APIRouter()


@router.post("/api/user")
def register_controller(user: schema.RegisterRequest, db: Session = Depends(get_db)):
    return User.register(user, db)


@router.patch("/api/user/update")
def register_controller(user: schema.UserUpdateRequest, X_API_TOKEN: Annotated[Union[str, None], Header()] = None, db: Session = Depends(get_db)):
    return User.updateUsers(user, X_API_TOKEN, db)
