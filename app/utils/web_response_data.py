from fastapi.responses import JSONResponse, Response
from app.schema import WebResponse
from typing import Union


def WebResponseData(data: Union[str, int, list, dict] = None, errors: str = None, code: int = 200):
    value = WebResponse(data=data, errors=errors)
    if code == 204:
        return Response(status_code=204)
    return JSONResponse(content=value.model_dump(), status_code=code)


# def WebResponseDataError(data: str = None, errors: str = None, code: int = 400):
#     value = WebResponse(data=data, errors=errors)
#     return JSONResponse(content=value.model_dump, status_code=code)
