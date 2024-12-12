
import os , json
from wsgiref import headers
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
import stripe
import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()

fees_router = APIRouter()

publish_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
secret_key = os.getenv('STRIPE_SECRET_KEY')
stripe.api_key = secret_key 
price_id = os.getenv('STRIPE_PRICE_ID')
webhook_secret = os.getenv('WEBHOOK_SECRET_KEY')

@fees_router.get("/examsubscription")
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
    
    
@fees_router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    body_bytes = await request.body()
    logging.info(f"Request body: {body_bytes.decode('utf-8')}")
    
    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print("Invalid payload")
        raise HTTPException(status_code=400, detail="Invalid payload")
    try:
        event = stripe.Webhook.construct_event(
            payload, headers.get("Stripe-Signature"), webhook_secret
        )
    except stripe.error.SignatureVerificationError as e:
        print("Invalid signature.")
        raise HTTPException(status_code=400, detail="Invalid signature.")
    if event["type"] == "checkout.session.completed":
        print("Checkout session completed")
        _object = event.get("data", {}).get("object", {})
        user_id = int(_object.get("metadata", {}).get("user_id"))
        amount_subtotal = _object.get("amount_subtotal", 0) / 100
        amount_total = _object.get("amount_total", 0) / 100
        quantity = _object.get("metadata", {}).get("quantity"),
        currency = _object.get("currency"),
        email = _object.get("customer_details", {}).get("email"),
        name = _object.get("customer_details", {}).get("name"),
        phone = _object.get("customer_details", {}).get("phone"),
        invoice_id = _object.get("invoice", None),
        city = _object.get("customer_details", {}).get("city", None),
        country = _object.get("customer_details", {}).get("country", None),
        line1 = _object.get("customer_details", {}).get("line1", None),
        line2 = _object.get("customer_details", {}).get("line2", None),
        postal_code = _object.get("customer_details", {}).get("postal_code", None),
        state = _object.get("customer_details", {}).get("state", None),
    elif event["type"] == "checkout.session.cancelled":
        print("Checkout session cancelled")
    elif event["type"] == "checkout.session.accepted":
        print("Checkout session accepted")
    elif event["type"] == "checkout.session.pending":
        print("Checkout session pending")
    return {}