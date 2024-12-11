
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.src.api.v1.users.services.forgotpass.forgotpass import forgotpassservices
from app.src.api.v1.users.services.loginusers.login import loginservices

user_router = APIRouter()

@user_router.post('/login', tags=["Login"])
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    return loginservices.login(db,form_data.username, form_data.password )

@user_router.post("/forgot-password", tags= ["forgot pass"])
def forgot_password(email: str, db: Session = Depends(get_db)):
    return forgotpassservices.forgot_password(email,db)
    
@user_router.post("/reset-password", tags= ["forgot pass"])
def reset_password(user_id: int, email: str, otp: str, new_password: str, db: Session = Depends(get_db)):
    return forgotpassservices.reset_password(user_id,email,otp,new_password,db)
