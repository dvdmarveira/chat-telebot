from fastapi import APIRouter, Depends, HTTPException
from src.models.models import Customer
from src.schemas.customer_schema import CustomerSchema
from sqlalchemy.orm import Session
from src.services.session_dependencies_service import get_session

customer_router = APIRouter(prefix="/api/customers", tags=["customers"])

@customer_router.get("/")
async def customers():
  """
  This is the default customers route. Only authorized users can access it.
  """
  return {"mensagem": "Hello customers"}

@customer_router.post("/customer")
async def create_customer(customer_schema: CustomerSchema, session: Session = Depends(get_session)):
  customer = session.query(Customer).filter(Customer.cellphone==customer_schema.cellphone).first()
  if customer:
    # Já existe um cliente com esse celular
    raise HTTPException(status_code=400, detail="cellphone already registered")
  else:
    new_customer = Customer(customer_schema.name, customer_schema.gender, customer_schema.address, customer_schema.cellphone)
    session.add(new_customer)
    session.commit()
    return {"message": f"Customer registered successfully. Customer ID: {new_customer.id}"}