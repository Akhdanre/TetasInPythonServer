from pydantic import BaseModel


class InkuTempRequest(BaseModel):
    condition: bool
    target_id: int
    target_token: str
    min_temp: int
    max_temp: int
