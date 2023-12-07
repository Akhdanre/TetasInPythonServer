from pydantic import BaseModel


class UserInkuRequest(BaseModel):
    id: str
    token:  str
    username: str
