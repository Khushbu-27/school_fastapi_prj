
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# from app.database.database import get_db
from app.src.api.v1.users.services.loginusers.login import loginservices
from app.src.api.v1.users.schemas.userschemas import AdminCreate
from app.src.api.v1.users.services.loginusers.loginwithphn import loginwithphnservices
from app.database.database import get_db

admin_router = APIRouter()

@admin_router.post("/admin/register", tags=["Login"])
def admin_register(admin: AdminCreate, db: Session = Depends(get_db)):
    return loginservices.admin_register(admin,db)

@admin_router.post("/login_with_phone", tags=["Login with phn"])
def login_with_phone_number(phone_number: str,db: Session = Depends(get_db)):
    return loginwithphnservices.login_with_phone_number(db, phone_number)

@admin_router.post("/verify_otp", tags=["Login with phn"])
def verify_otp(phone_number: str, otp: int,db: Session = Depends(get_db)):
    return loginwithphnservices.verify_otp(db, phone_number, otp)