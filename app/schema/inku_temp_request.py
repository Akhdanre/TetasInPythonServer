from pydantic import BaseModel

class InkuTempRequest(BaseModel):
    min_temp : int
    max_temp : int