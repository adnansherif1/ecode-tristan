from pydantic import BaseModel, conlist
from typing import List, Any


class DataInput(BaseModel):
    html: List[List[Any]]
    user_data: Any
#     data:List[List[str,str,str,List[]]]


class PredictionResponse(BaseModel):
    out: Any