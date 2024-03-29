from fastapi import HTTPException
from fastapi import Request, status
from fastapi.responses import JSONResponse
from schema import WebResponse


class ExceptionCustom(HTTPException):
    pass


def exception_400_handler(request: Request, exc: ExceptionCustom):
    response_content = WebResponse(errors=exc.detail)
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response_content.model_dump())


def exception_401_handler(request: Request, exc: ExceptionCustom):
    response_content = WebResponse(errors=exc.detail)
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=response_content.model_dump())
