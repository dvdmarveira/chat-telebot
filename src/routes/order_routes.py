from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.services.session_dependency_service import get_session
from src.services.verify_token_dependency_service import verify_token
from src.schemas.order_schema import OrderSchema
from src.schemas.item_order_schema import ItemOrderSchema
from src.schemas.order_response_schema import OrderResponseSchema
from src.models.models import Order, User, Order_Items
from typing import List, Optional

order_router = APIRouter(prefix="/api/orders", tags=["orders"], dependencies=[Depends(verify_token)])

@order_router.get("/") #/api/orders
async def get_orders(
  customer_id: Optional[int] = Query(None, description="Filter orders by customer ID"), 
  user_id: Optional[int] = Query(None, description="Filter orders by user ID"),
  session: Session = Depends(get_session), 
  user: User = Depends(verify_token)):
  if not user.admin:
    raise HTTPException(status_code=401, detail="Authorization denied")
  
  query = session.query(Order)
  if customer_id is not None:
    query = query.filter(Order.customer==customer_id)
  elif user_id is not None:
    query = query.filter(Order.user==user_id)
    
  orders = query.all()
  return {
    "orders": orders
    }
  # else:
  #   orders = session.query(Order).all()
  #   return {
  #     "orders": orders
  #   }
    
@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session: Session = Depends(get_session)):
  if order_schema.user is not None:
    user = session.get(User, order_schema.user)
    if user is None:
      raise HTTPException(status_code=400, detail="User not found")
    user_id = user.id
  else:
    user_id = None
  new_order = Order(customer=order_schema.customer, user=user_id)
  session.add(new_order)
  session.commit()
  session.refresh(new_order)

  return {"message": f"Order created successfully. Order ID: {new_order.id}"}

@order_router.get("/order/{id_order}")
async def get_order_by_id(id_order: int, 
                          session: Session = Depends(get_session), 
                          user: User = Depends(verify_token)):
  order = session.query(Order).filter(Order.id==id_order).first()
  if not order:
    raise HTTPException(status_code=400, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=401, detail="Authorization denied")
  return {
    "order_items_quantity": len(order.items),
    "order": order
  }
  
# @order_router.get("/customer/{id_customer}", response_model=List[OrderResponseSchema])
# async def get_orders_by_customer(id_customer: int,
#                                  session: Session = Depends(get_session), 
#                                  user: User = Depends(verify_token)):
#   if not user.admin:
#     raise HTTPException(status_code=401, detail="Authorization denied") 
#   orders_list = session.query(Order).filter(Order.customer==id_customer).all()
#   return orders_list

# @order_router.get("/user/{id_user}", response_model=List[OrderResponseSchema])
# async def get_orders_by_user(id_user: int,
#                              session: Session = Depends(get_session),
#                              user: User = Depends(verify_token)):
#   if not user.admin:
#     raise HTTPException(status_code=401, detail="Authorization denied")
#   orders_list = session.query(Order).filter(Order.user==id_user).all()
#   return orders_list

@order_router.patch("/order/{id_order}")
async def cancel_order(id_order: int, 
                       session: Session = Depends(get_session), 
                       user: User = Depends(verify_token)):
  order = session.query(Order).filter(Order.id==id_order).first()
  if not order:
    raise HTTPException(status_code=404, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=403, detail="Authorization denied")
  
  if order.status == "CANCELLED":
    return {
      "message": f"Order ID:{order.id} is already cancelled.",
      "order": order
    }
    
  order.status = "CANCELLED"
  session.commit()
  
  return {
    "message": f"Order ID:{order.id} has been cancelled successfully.",
    "order": order
  }
  
@order_router.post("/order/item/{id_order}/add")
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
    "message": f"Item added successfully to order number {id_order}",
    "item_id": item_order.id,
    "order_price": order.price 
  }
  
@order_router.post("/order/item/{id_order_item}/remove")
async def remove_order_item(id_order_item: int, 
                         session: Session = Depends(get_session), 
                         user: User = Depends(verify_token)):
  order_item = session.query(Order_Items).filter(Order_Items.id==id_order_item).first()
  order = session.query(Order).filter(Order.id==order_item.order).first()
  if not order_item:
    raise HTTPException(status_code=400, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=401, detail="Authorization denied")
  session.delete(order_item)
  order.calculate_price()
  session.commit()
  return {
    "message": "Item removed successfully",
    "order_items_quantity": len(order.items),
    "order": order
  }
  
@order_router.post("/order/{id_order}/complete")
async def complete_order(id_order: int, 
                       session: Session = Depends(get_session), 
                       user: User = Depends(verify_token)):
  order = session.query(Order).filter(Order.id==id_order).first()
  if not order:
    raise HTTPException(status_code=400, detail="Order not found")
  if not user.admin and user.id != order.customer:
    raise HTTPException(status_code=401, detail="Authorization denied")
  order.status = "COMPLETED"
  session.commit()
  return {
    "message": f"Order ID:{order.id} has been completed successfully.",
    "order_items_quantity": len(order.items),
    "order": order
  }
