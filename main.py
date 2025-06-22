from fastapi import FastAPI

app = FastAPI()

from src.routes.auth_routes import auth_router
from src.routes.order_routes import order_router
from src.routes.customer_routes import customer_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(customer_router)





# uvicorn main:app --reload