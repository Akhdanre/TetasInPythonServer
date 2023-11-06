from fastapi import FastAPI, Header, HTTPException
from typing import Annotated, Union
from pydantic import BaseModel
import uvicorn

app = FastAPI()



# entity
class Contact(BaseModel):
    email: str
    name: str

class ContactModel:
    def __init__(self, email, name, token):
        self.email = email
        self.name = name
        self.token = token

userData = []
userData.append(ContactModel("oukenzeuma@gmail.com", "oukenze", "k1i34hh45987skjy4b"))
userData.append(ContactModel("akeonfoo@gmail.com", "akeon", "t12kh34b6l285b56l23f5v"))


class AuthHandler:
    def __init__(self, api_tokens):
        self.api_tokens = api_tokens

    def is_valid_token(self, token):
        return token in self.api_tokens


@app.post("/protected-endpoint")
async def protected_endpoint(contact: Contact, X_API_TOKEN: Annotated[Union[str, None], Header()] = None):
    if X_API_TOKEN is None or not auth_handler.is_valid_token(X_API_TOKEN):
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"message": "Access granted to the protected endpoint", "contact": contact}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
