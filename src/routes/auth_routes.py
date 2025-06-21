from fastapi import APIRouter, Depends, HTTPException
from src.models.models import User
from src.services.session_dependencies_service import get_session
from main import bcrypt_context
from src.schemas.user_schema import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate():
  """
  This is the default authentication route
  """
  return {"oi"}

@auth_router.post("/sign_up")
async def sign_up(user_schema: UserSchema, session: Session = Depends(get_session)):

  user = session.query(User).filter(User.email==user_schema.email).first()
  if user:
    # Já existe usuário com esse e-mail
    raise HTTPException(status_code=400, detail="email already exists")
  else:
    cryptography_password = bcrypt_context.hash(user_schema.password)
    new_user = User(user_schema.name, user_schema.email, cryptography_password, user_schema.gender, user_schema.admin, user_schema.active)
    session.add(new_user)
    session.commit()
    return {"message": f"user registered successfully {user_schema.email}"}