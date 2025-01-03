
import os , json
from wsgiref import headers
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
import stripe
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

sub_router = APIRouter()

publish_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = secret_key 
price_id = os.getenv('STRIPE_PRICE_ID')
webhook_secret = os.getenv('WEBHOOK_SECRET_KEY')

@sub_router.get("/examsubscription")
def get_exam_subscription():

    checkout_session = stripe.checkout.Session.create(
       
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        # allow_promotion_codes=True,
        # invoice_creation=stripe.checkout.Session.CreateParamsInvoiceCreation(
        #     enabled=True
        # ),
        metadata={
            "user_id": 1,
            "email": "user@example.com",
            "quantity": 1,
        },
        mode="subscription",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
        customer_email="user@example.com",
    )
    return {
        "url": checkout_session.url
    }

@sub_router.get("/success")
def success_page():
    return {"message": "Subscription successful!"}

@sub_router.get("/cancel")
def cancel_page():
    return {"message": "Subscription was canceled."}

    
@sub_router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    
    logging.info(f"Webhook payload: {payload.decode('utf-8')}")

    sig_header = request.headers.get("Stripe-Signature")
    logging.info(f"Stripe-Signature: {sig_header}")
    
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=webhook_secret
        )
    except ValueError as e:
        logging.error("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        logging.error("Invalid signature")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=400, detail="Unexpected error")
    
    if event["type"] == "checkout.session.completed":
        logging.info("Checkout session completed")
        _object = event.get("data", {}).get("object", {})
    else:
        logging.info(f"Unhandled event type: {event['type']}")

    return {"status": "success"}

    
# @sub_router.post("/webhook")
# async def stripe_webhook(request: Request):
    
#     stripe.WebhookEndpoint.list(limit=3)

#     payload = await request.body()
    
#     logging.info(f"Request body: {payload.decode('utf-8')}")
#     event = None
    
#     try:
#         event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
#     except ValueError as e:
#         print("Invalid payload")
#         raise HTTPException(status_code=400, detail="Invalid payload")
    
#     except stripe.error.SignatureVerificationError as e:
#         print("Invalid signature")
#         raise HTTPException(status_code=400, detail="Invalid signature")
    
#     if event["type"] == "checkout.session.completed":
#         print("Checkout session completed")
#         _object = event.get("data", {}).get("object", {})
        
#     elif event["type"] == "checkout.session.cancelled":
#         print("Checkout session cancelled")
#     elif event["type"] == "checkout.session.accepted":
#         print("Checkout session accepted")
#     elif event["type"] == "checkout.session.pending":
#         print("Checkout session pending")
        
#     return {}