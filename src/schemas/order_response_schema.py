from pydantic import BaseModel 
from typing import List
from src.schemas.item_order_schema import ItemOrderSchema

class OrderResponseSchema(BaseModel):
  id: int
  price: float
  status: str
  items: List[ItemOrderSchema]
  
  class Config:
    from_attributes = True