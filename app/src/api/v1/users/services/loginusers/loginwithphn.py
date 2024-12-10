
from fastapi import APIRouter, HTTPException
import os
from requests import Session
from app.src.api.v1.users.models.usersmodel import User
from twilio.rest import Client
from dotenv import load_dotenv
import random
from app.src.api.v1.users.services.user_authentication.user_auth import create_access_token
from app.src.api.v1.utils.response_utils import Response


load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

otp_storage = {}

class loginwithphnservices:
    
    # LOGIN WITH PHONE NUMBER (ONLY ADMIN)
    def login_with_phone_number(db: Session, phone_number: str):
        
        user = db.query(User).filter(User.phone_number == phone_number, User.role == "admin").first()

        if not user:
            return Response(
                status_code=401,
                message="Phone number not registered or not an admin",
                data={}
            ).send_error_response()

        otp = random.randint(100000, 999999)  
        otp_message = f"Your OTP code is: {otp}"

        try:
            message = client.messages.create(
                body=otp_message,
                from_=twilio_phone_number,
                to=phone_number
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Twilio error: {str(e)}")

        user.otp = otp  
        db.commit()

        return Response(
            status_code=200,
            message="OTP sent successfully",
            data={"otp": "OTP sent to phone number"}
        ).send_success_response()

    # VERIFY OTP
    def verify_otp(db: Session, phone_number: str, otp: int):
    
        user = db.query(User).filter(User.phone_number == phone_number, User.role == "admin").first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        if user.otp != otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        access_token = create_access_token(data={"sub": user.username, "role": user.role})
        
        response_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "access_token": access_token,
            "token_type": "Bearer",
        }
        
        return Response(
            status_code=200,
            message="Phone number login successful",
            data=response_data
        ).send_success_response()