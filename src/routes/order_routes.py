from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.services.session_dependencies_service import get_session
from src.schemas.order_schema import OrderSchema
from src.models.models import Order

order_router = APIRouter(prefix="/api/orders", tags=["orders"])

@order_router.get("/")
async def orders():
  """
  This is the default orders route. Only authorized users can access it.
  """
  return {"mensagem": "Hello orders"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
  new_order = Order(customer=order_schema.customer)
  session.add(new_order)
  session.commit()
  return {"message": f"Order created successfully. Order ID: {new_order.id}"}