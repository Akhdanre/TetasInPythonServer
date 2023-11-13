from pydantic import BaseModel


class InkuTempRequest(BaseModel):
    target_id: int
    target_token: str
    temp_limit: int
    humd_limit: int
