

from pydantic import BaseModel


class StartIncubateRequest(BaseModel):
    id_inkubator: int
    start_date: str
    number_of_egg: int
