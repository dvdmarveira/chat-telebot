from pydantic import BaseModel

class OrderSchema(BaseModel):
  customer: int
  
  class Config:
    from_attributes = True