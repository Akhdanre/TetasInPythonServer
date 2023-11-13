from pydantic import BaseModel


class InkuTempRequest(BaseModel):
    target_id: int
    target_token: str
    min_temp: int
    max_temp: int
    min_humd: int
    max_humd: int
