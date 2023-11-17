

from pydantic import BaseModel


class StartIncubateRequest(BaseModel):
    id_inkubator: int
    name: str
    start_date: str
    number_of_egg: int
