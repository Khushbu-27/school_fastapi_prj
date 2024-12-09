
from fastapi import APIRouter
import os
from twilio.rest import Client
from dotenv import load_dotenv
import random

router = APIRouter()

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
phone_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)

otp_storage = {}

# router.post("/send_otp/")
# def send_otp(phone:phone)
