from fastapi import APIRouter, Depends, Header
import app.schema as schema
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from app.service import auth_service


route = APIRouter()


@route.post("/api/authentication")
def authRoute(request : schema.AuthRequest, db : Session = Depends(get_db)):
    return auth_service.Authetication.login(request, db)