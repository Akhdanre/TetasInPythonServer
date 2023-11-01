# models.py
from pydantic import BaseModel

class Item(BaseModel):
    message: str
