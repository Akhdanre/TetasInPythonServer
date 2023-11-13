from pydantic import BaseModel


class InkuTempRequest(BaseModel):
    condition: bool
    target_id: str
    target_token: str
    min_temp: int
    max_temp: int
