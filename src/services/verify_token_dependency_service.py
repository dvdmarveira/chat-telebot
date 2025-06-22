from fastapi import Depends, HTTPException
from src.configs.config import SECRET_KEY, ALGORITHM, oauth2_schema
from src.services.session_dependency_service import get_session
from sqlalchemy.orm import Session
from src.models.models import User
from jose import jwt, JWTError

def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
  try:
    dictionary_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
    id_user = dictionary_info.get("sub")
  except JWTError:
    raise HTTPException(status_code=401, detail="Access denied. Check token validity")
  # Verificar se o token é válido
  # Extrair o ID do usuário do token
  user = session.query(User).filter(User.id==id_user).first()
  if not user:
    raise HTTPException(status_code=401, detail="Invalid access")
  return user