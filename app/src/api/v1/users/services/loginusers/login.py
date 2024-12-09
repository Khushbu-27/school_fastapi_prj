from datetime import date
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.src.api.v1.users.models.usersmodel import User
from app.src.api.v1.users.schemas.userschemas import AdminCreate
from app.src.api.v1.users.services.user_authentication.user_auth import create_access_token, get_password_hash, verify_password
from app.src.api.v1.utils.response_utils import Response


class loginservices:

    #ADMIN REGISTRATION
    def admin_register(admin: AdminCreate, db: Session ):

        if admin.password != admin.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match"
            )
        
        if db.query(User).filter(User.username == admin.username).first():
            raise HTTPException(status_code=400, detail="Username already registered")
        
        if db.query(User).filter(User.email == admin.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = get_password_hash(admin.password)
        new_admin = User(
            username=admin.username,
            email=admin.email,
            hashed_password=hashed_password,
            phone_number=admin.phone_number, 
            role="admin"
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        
        response_data = {
                "username": admin.username,
                "email": admin.email,
                "phone": admin.phone_number,
                "role": new_admin.role,
            }
        return Response(
                status_code=201,
                message="Admin registered successfully",
                data= response_data 
            ).send_success_response()

    
    #USER LOGIN
    def login(db: Session, username: str, password: str):
    
        user = db.query(User).filter(User.username == username).first()
        
        if not user or not verify_password(password, user.hashed_password):   
            return Response(
                status_code=401,
                message="User not found",
                data= {}
            ).send_error_response()

        today = date.today()

        if user.role == "admin":
            access_token = create_access_token(data={"sub": user.username, "role": "admin"})
            
            response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "access_token": access_token,
                "token_type": "Bearer",
            }
            return Response(
                status_code=201,
                message="Admin login successfully",
                data= response_data 
            ).send_success_response()

        elif user.role in ["teacher", "student"]:
            
            if user.last_login_date != today:
                user.attendance += 1
                user.last_login_date = today    
            db.commit() 

            access_token = create_access_token(data={"sub": user.username})
            
            response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "access_token": access_token,
                "token_type": "Bearer",
            }
            return Response(
                status_code=201,
                message=f"{user.role.capitalize()} login successful",
                data= response_data 
            ).send_success_response()
            