from fastapi.responses import JSONResponse
from app.schema import WebResponse


def WebResponseData(atr: WebResponse, code: int = 200):
    return JSONResponse(content=atr.model_dump, status_code=code)



def WebResponseDataError(atr: WebResponse, code: int = 400):
    return JSONResponse(content=atr.model_dump, status_code=code)
