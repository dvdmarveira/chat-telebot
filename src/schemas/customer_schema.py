from pydantic import BaseModel
from typing import Optional

class CustomerSchema(BaseModel):
  name: str 
  gender: Optional[str]
  address: Optional[str]
  cellphone: str
  
  class Config:
    from_attributes = True