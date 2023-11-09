from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.deps import get_db
from schema.register_request import RegisterRequest
from service.user_service import User

router = APIRouter()


@router.post("/api/register")
def register_controller(user: RegisterRequest, db: Session = Depends(get_db)):
    return User.register(user,db)
     

