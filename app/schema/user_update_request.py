from pydantic import BaseModel

class UserUpdateRequest(BaseModel):
    password : str
    name : str