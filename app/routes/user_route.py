from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import sys

sys.path.append("..")
from app.utils.deps import get_db
from app.schema.register_request import RegisterRequest
from app.service.user_service import User

router = APIRouter()


@router.post("/api/register")
def register_controller(user: RegisterRequest, db: Session = Depends(get_db)):
    return User.register(user,db)
     

