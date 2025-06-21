from fastapi import APIRouter
from src.models.models import db, User
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
  """
  This is the default authentication route
  """
  return {"oi"}

@auth_router.post("/sign_up")
async def sign_up(name: str, email: str, password: str, gender: str):
  Session = sessionmaker(bind=db)
  session = Session()
  user = session.query(User).filter(User.email==email).first()
  if user:
    # Já existe usuário com esse e-mail
    return {"message": "email already exists"}
  else:
    new_user = User(name, email, password, gender)
    session.add(new_user)
    session.commit()
    return {"message": "user registered successfully"}