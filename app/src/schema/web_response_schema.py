from pydantic import BaseModel
from typing import Union, List, Optional

class WebResponse(BaseModel):
    data: Optional[Union[int, str, List]] = None
    errors:  Optional[str] = None