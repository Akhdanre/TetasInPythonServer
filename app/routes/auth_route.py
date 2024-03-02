from fastapi import APIRouter, Depends, Header
import schema as schema
from sqlalchemy.orm import Session
from utils.deps import get_db
from service import auth_service
from typing import Annotated, Union


route = APIRouter()


@route.post("/api/authentication")
def authRoute(request : schema.AuthRequest, db : Session = Depends(get_db)):
    return auth_service.Authetication.login(request, db)


@route.get("/api/logout")
def logoutRoute(X_API_TOKEN : Annotated[Union[str, None], Header()] = None, db : Session = Depends(get_db)):
    return auth_service.Authetication.logout(X_API_TOKEN, db)