
import datetime
import random
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.src.api.v1.users.services.crud.createusers import User
from app.src.api.v1.users.services.user_authentication.user_auth import get_password_hash
from app.src.api.v1.users.utils import emailutils
from app.src.api.v1.utils.response_utils import Response

otp_store = {}
otp_expiry_time = 300 


class forgotpassservices:

    # FORGOT PASSWORD
    def forgot_password(email: str, db: Session):
        email = email.strip().lower()  
        otp = str(random.randint(100000, 999999))  
        otp_store[email] = {"otp": otp, "timestamp": datetime.now()}
        print(f"Stored OTP for {email}: {otp_store[email]}")
        emailutils.send_otp_email(email, otp)  
        return {"message": "OTP sent to email"}

    # RESET PASSWORD
    def reset_password(user_id: int, email: str, otp: str, new_password: str, db: Session):
        email = email.strip().lower() 

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="Invalid user ID or email")

        if email not in otp_store:
            print(f"Available OTP store keys: {otp_store.keys()}")  
            raise HTTPException(status_code=400, detail="OTP not requested")
        
        otp_data = otp_store[email]

        if (datetime.now() - otp_data["timestamp"]).total_seconds() > otp_expiry_time:
            del otp_store[email]
            raise HTTPException(status_code=400, detail="OTP expired")
        
        if otp_data["otp"] != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        hashed_password = get_password_hash(new_password)
        user.hashed_password = hashed_password
        db.commit()

        del otp_store[email]  
        
        response_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "password": user.hashed_password
            }
        return Response(
                status_code=201,
                message=" Password reset successfully",
                data= response_data 
            ).send_success_response()
