from pydantic import BaseModel, validator


class UserSchema(BaseModel):
    username: str 
    password: str
    name: str

 