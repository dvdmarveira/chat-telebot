from pydantic import BaseModel
from typing import Optional
class OrderSchema(BaseModel):
  customer: int
  user: Optional[int] = None
  
  class Config:
    from_attributes = True