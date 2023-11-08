from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from schema.web_response_schema import WebResponse


router = APIRouter()


@router.get("/api/register")
def registerController():
    return JSONResponse(status_code=200, content=WebResponse(data="ok").model_dump())
