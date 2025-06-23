from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.services.session_dependency_service import get_session
from src.services.verify_token_dependency_service import verify_token
from src.schemas.order_schema import OrderSchema
from src.schemas.item_order_schema import ItemOrderSchema
from src.models.models import Order, User, Order_Items

order_router = APIRouter(prefix="/api/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/") #/api/orders
async def get_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
  if not user.admin:
    raise HTTPException(status_code=401, detail="Authorization denied")
  else:
    orders = session.query(Order).all()
    return {
      "orders": orders
    }
    
@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
  new_order = Order(customer=order_schema.customer)
  session.add(new_order)
  session.commit()
  return {"message": f"Order created successfully. Order ID: {new_order.id}"}

@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, 
                       session: Session = Depends(get_session), 
                       user: User = Depends(verify_token)):
  order = session.query(Order).filter(Order.id==id_order).first()
  if not order:
    raise HTTPException(status_code=400, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=401, detail="Authorization denied")
  order.status = "CANCELLED"
  session.commit()
  
  return {
    "message": f"Order ID:{order.id} has been cancelled successfully.",
    "order": order
  }
  
@order_router.post("/order/item/add/{id_order}")
async def add_order_item(id_order: int, 
                         item_order_schema: ItemOrderSchema, 
                         session: Session = Depends(get_session), 
                         user: User = Depends(verify_token)):
  order = session.query(Order).filter(Order.id==id_order).first()
  if not order:
    raise HTTPException(status_code=400, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=401, detail="Authorization denied")
  item_order = Order_Items(item_order_schema.amount, 
                           item_order_schema.flavor, 
                           item_order_schema.unit_price, 
                           id_order)
  session.add(item_order)
  order.calculate_price()
  session.commit()
  return {
    "message": "Created item successfully",
    "item_id": item_order.id,
    "order_price": order.price 
  }
  