from pydantic import BaseModel
from datetime import datetime

class AddDetailHatchRequest(BaseModel): 
    id_hatch_data : int
    temp : int
    humd : int
    water_volume : int

    
