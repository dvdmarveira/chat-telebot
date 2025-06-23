from fastapi import APIRouter, Depends, HTTPException
from src.models.models import User
from src.services.session_dependency_service import get_session
from src.services.verify_token_dependency_service import verify_token
from src.configs.config import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from src.schemas.user_schema import UserSchema
from src.schemas.login_schema import LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

def create_token(id_user, token_duration=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
  expiration_date = datetime.now(timezone.utc) + token_duration
  expiration_timestamp = int(expiration_date.timestamp())
  dictionary_info = {"sub": str(id_user),
                     "expiration": expiration_timestamp} # se fosse 'exp' seria reconhecido pelo JWT automaticamente
  encoded_jwt = jwt.encode(dictionary_info, SECRET_KEY, ALGORITHM )
  return encoded_jwt

def authenticate_user(email, password, session):
  user = session.query(User).filter(User.email==email).first()
  if not user:
    return False
  elif not bcrypt_context.verify(password, user.password):
    return False
  return user
  
@auth_router.post("/sign_up")
async def sign_up(user_schema: UserSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):
  if not user.admin:
    raise HTTPException(status_code=401, detail="Authorization denied")
  existing_user = session.query(User).filter(User.email==user_schema.email).first()
  if existing_user:
    # Já existe usuário com esse e-mail
    raise HTTPException(status_code=400, detail="email already exists")
  else:
    cryptography_password = bcrypt_context.hash(user_schema.password)
    new_user = User(user_schema.name, user_schema.email, cryptography_password, user_schema.gender, user_schema.admin, user_schema.active)
    session.add(new_user)
    session.commit()
    return {"message": f"user registered successfully {user_schema.email}"}
  
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
  user = authenticate_user(login_schema.email, login_schema.password, session)
  if not user:
    raise HTTPException(status_code=400, detail="user not registered or invalid credentials")
  else:
    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_duration=timedelta(days=7))
    return {"access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"}
    
@auth_router.post("/login-form") # Para testar rotas protegidas pela doc nativa FastAPI
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
  user = authenticate_user(form_data.username, form_data.password, session)
  if not user:
    raise HTTPException(status_code=400, detail="user not registered or invalid credentials")
  else:
    access_token = create_token(user.id)
    return {"access_token": access_token,
            "token_type": "Bearer"}
    
@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
  access_token = create_token(user.id)
  return {
    "access_token": access_token,
    "token_type": "Bearer"
  }