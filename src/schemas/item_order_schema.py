from pydantic import BaseModel 
from typing import Optional

class ItemOrderSchema(BaseModel):
  amount: int
  flavor: str
  unit_price: float
  
  class Config:
    from_attributes = True