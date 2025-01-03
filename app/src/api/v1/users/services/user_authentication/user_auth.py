
from datetime import datetime, time, timedelta
import os
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, Request, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.users.models.usersmodel import User
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM =os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
def decode_access_token(token: str): 
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token is invalid or expired: {str(e)}")
    
def token_response(token: str):
    return {
        "access_token": token
    }
    
class JWTBearer(HTTPBearer):
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials or credentials.scheme != "Bearer": 
            raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
        
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid or expired token.")
        return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            decode_access_token(jwtoken)
            return True                                                                              
        except HTTPException:
            return False

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# ROLE BASE AUTHENTICATION
def authorize_admin(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    
    payload = decode_access_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin authorization required")
    return payload

def authorize_user(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    
    payload = decode_access_token(token)
    username = payload.get("sub")
    
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if user.role not in ["admin", "teacher", "student"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid role")

    return user
