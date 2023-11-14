from fastapi import Request, status
from fastapi.responses import JSONResponse
from utils.exception_handler import ExceptionCustom


def exception_400_handler(request: Request, exc: ExceptionCustom):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"errors": exc.detail})
