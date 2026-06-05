from fastapi import FastAPI, APIRouter, HTTPException, Header, Request, Response, Cookie, UploadFile, File, Query, Depends
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import stripe
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import requests

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY', '')
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', '')
APP_NAME = os.environ.get('APP_NAME', 'playbeat-digital')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://playbeat.digital')
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')

stripe.api_key = STRIPE_API_KEY

app = FastAPI()
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# ── Models ────────────────────────────────────────────────────────────────────

class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    role: str = "admin"
    created_at: str

class Customer(BaseModel):
    customer_id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    status: str = "active"
    wallet_balance: float = 0.0
    created_at: str
    last_login: Optional[str] = None

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None

class Product(BaseModel):
    product_id: str
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    category: Optional[str] = None
    product_type: str = "digital_download"
    is_visible: bool = True
    image_url: Optional[str] = None
    created_at: str

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discount_price: Optional[float] = None
    category: Optional[str] = None
    product_type: str = "digital_download"
    is_visible: bool = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    discount_price: Optional[float] = None
    category: Optional[str] = None
    is_visible: Optional[bool] = None

class Order(BaseModel):
    order_id: str
    customer_id: str
    product_id: str
    amount: float
    status: str = "pending"
    payment_status: str = "pending"
    transaction_id: Optional[str] = None
    created_at: str

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None

class DashboardStats(BaseModel):
    total_revenue: float
    monthly_revenue: float
    daily_revenue: float
    total_customers: int
    active_customers: int
    new_registrations: int
    total_orders: int
    pending_orders: int
    completed_orders: int

class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = 1

class Cart(BaseModel):
    items: List[CartItem]
    total: float

class PaymentIntentRequest(BaseModel):
    amount: float

class ConfirmPaymentRequest(BaseModel):
    client_secret: str
    card: Optional[Dict[str, Any]] = None

class OrderCreate(BaseModel):
    items: List[Dict[str, Any]]
    total: float
    payment_intent_id: str


# ── Auth helpers ──────────────────────────────────────────────────────────────

def get_session_token(authorization: Optional[str] = None, session_token_cookie: Optional[str] = None) -> Optional[str]:
    if session_token_cookie:
        return session_token_cookie
    if authorization and authorization.startswith("Bearer "):
        return authorization.replace("Bearer ", "")
    return None

async def get_current_user(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)) -> User:
    token = get_session_token(authorization, session_token)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_doc = await db.user_sessions.find_one({"session_token": token}, {"_id": 0})
    if not session_doc:
        raise HTTPException(status_code=401, detail="Invalid session")

    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")

    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")

    return User(**user_doc)


# ── Auth routes ───────────────────────────────────────────────────────────────

@api_router.post("/auth/session")
async def create_session(request: Request):
    data = await request.json()
    session_id = request.headers.get("X-Session-ID") or data.get("session_id")

    if not session_id:
        raise HTTPException(status_code=400, detail="session_id required")

    try:
        resp = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": session_id},
            timeout=10
        )
        resp.raise_for_status()
        oauth_data = resp.json()
    except Exception as e:
        logger.error(f"OAuth session exchange failed: {e}")
        raise HTTPException(status_code=400, detail="Invalid session_id")

    user_id = f"user_{uuid.uuid4().hex[:12]}"
    existing_user = await db.users.find_one({"email": oauth_data["email"]}, {"_id": 0})

    if existing_user:
        user_id = existing_user["user_id"]
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"name": oauth_data["name"], "picture": oauth_data.get("picture")}}
        )
    else:
        await db.users.insert_one({
            "user_id": user_id,
            "email": oauth_data["email"],
            "name": oauth_data["name"],
            "picture": oauth_data.get("picture"),
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat()
        })

    session_token = oauth_data["session_token"]
    await db.user_sessions.insert_one({
        "user_id": user_id,
        "session_token": session_token,
        "expires_at": datetime.now(timezone.utc) + timedelta(days=7),
        "created_at": datetime.now(timezone.utc).isoformat()
    })

    user_doc = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    response = JSONResponse(content={"user": user_doc})
    response.set_cookie(
        key="session_token", value=session_token,
        httponly=True, secure=True, samesite="none", path="/", max_age=7*24*60*60
    )
    return response

@api_router.get("/auth/me", response_model=User)
async def get_me(authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    return await get_current_user(authorization, session_token)

@api_router.post("/auth/logout")
async def logout(response: Response, authorization: Optional[str] = Header(None), session_token: Optional[str] = Cookie(None)):
    token = get_session_token(authorization, session_token)
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out"}


# ── Dashboard ─────────────────────────────────────────────────────────────────

@api_router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_user)):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_orders = await db.orders.count_documents({})
    completed_orders = await db.orders.find({"payment_status": "paid"}, {"_id": 0}).to_list(None)

    total_revenue = sum(o.get("amount", 0) for o in completed_orders)
    monthly_revenue = sum(o.get("amount", 0) for o in completed_orders if o.get("created_at") and datetime.fromisoformat(o["created_at"]) >= month_start)
    daily_revenue = sum(o.get("amount", 0) for o in completed_orders if o.get("created_at") and datetime.fromisoformat(o["created_at"]) >= today_start)

    total_customers = await db.customers.count_documents({})
    active_customers = await db.customers.count_documents({"status": "active"})
    new_registrations = await db.customers.count_documents({"created_at": {"$gte": month_start.isoformat()}})
    pending_orders = await db.orders.count_documents({"status": "pending"})
    completed_count = await db.orders.count_documents({"status": "completed"})

    return DashboardStats(
        total_revenue=total_revenue, monthly_revenue=monthly_revenue, daily_revenue=daily_revenue,
        total_customers=total_customers, active_customers=active_customers, new_registrations=new_registrations,
        total_orders=total_orders, pending_orders=pending_orders, completed_orders=completed_count
    )


# ── Customers ─────────────────────────────────────────────────────────────────

@api_router.get("/customers", response_model=List[Customer])
async def get_customers(current_user: User = Depends(get_current_user)):
    return await db.customers.find({}, {"_id": 0}).to_list(1000)

@api_router.post("/customers", response_model=Customer)
async def create_customer(customer: CustomerCreate, current_user: User = Depends(get_current_user)):
    doc = {"customer_id": f"cust_{uuid.uuid4().hex[:12]}", **customer.model_dump(), "status": "active", "wallet_balance": 0.0, "created_at": datetime.now(timezone.utc).isoformat()}
    await db.customers.insert_one(doc)
    return Customer(**doc)

@api_router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: str, current_user: User = Depends(get_current_user)):
    doc = await db.customers.find_one({"customer_id": customer_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(**doc)

@api_router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: str, update: CustomerUpdate, current_user: User = Depends(get_current_user)):
    data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No data to update")
    result = await db.customers.update_one({"customer_id": customer_id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return Customer(**await db.customers.find_one({"customer_id": customer_id}, {"_id": 0}))

@api_router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: str, current_user: User = Depends(get_current_user)):
    result = await db.customers.delete_one({"customer_id": customer_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}


# ── Products ──────────────────────────────────────────────────────────────────

@api_router.get("/products", response_model=List[Product])
async def get_products():
    return await db.products.find({}, {"_id": 0}).to_list(1000)

@api_router.post("/products", response_model=Product)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    doc = {"product_id": f"prod_{uuid.uuid4().hex[:12]}", **product.model_dump(), "created_at": datetime.now(timezone.utc).isoformat()}
    await db.products.insert_one(doc)
    return Product(**doc)

@api_router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    doc = await db.products.find_one({"product_id": product_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**doc)

@api_router.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, update: ProductUpdate, current_user: User = Depends(get_current_user)):
    data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No data to update")
    result = await db.products.update_one({"product_id": product_id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return Product(**await db.products.find_one({"product_id": product_id}, {"_id": 0}))

@api_router.delete("/products/{product_id}")
async def delete_product(product_id: str, current_user: User = Depends(get_current_user)):
    result = await db.products.delete_one({"product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


# ── Orders ────────────────────────────────────────────────────────────────────

@api_router.get("/orders", response_model=List[Order])
async def get_orders(current_user: User = Depends(get_current_user)):
    return await db.orders.find({}, {"_id": 0}).sort("created_at", -1).to_list(1000)

@api_router.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str, current_user: User = Depends(get_current_user)):
    doc = await db.orders.find_one({"order_id": order_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**doc)

@api_router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: str, update: OrderUpdate, current_user: User = Depends(get_current_user)):
    data = {k: v for k, v in update.model_dump().items() if v is not None}
    if not data:
        raise HTTPException(status_code=400, detail="No data to update")
    result = await db.orders.update_one({"order_id": order_id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return Order(**await db.orders.find_one({"order_id": order_id}, {"_id": 0}))


# ── Payments (native Stripe) ──────────────────────────────────────────────────

@api_router.post("/payments/checkout")
async def create_checkout(request: Request, current_user: User = Depends(get_current_user)):
    data = await request.json()
    package_id = data.get("package_id")
    origin_url = data.get("origin_url", FRONTEND_URL)

    PACKAGES = {"small": 5.0, "medium": 10.0, "large": 20.0}
    if package_id not in PACKAGES:
        raise HTTPException(status_code=400, detail="Invalid package")

    amount = PACKAGES[package_id]
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {"currency": "usd", "product_data": {"name": f"Playbeat {package_id.title()} Package"}, "unit_amount": int(amount * 100)}, "quantity": 1}],
            mode="payment",
            success_url=f"{origin_url}/payment/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{origin_url}/payment/cancel",
            metadata={"package_id": package_id, "user_id": current_user.user_id}
        )
    except Exception as e:
        logger.error(f"Stripe checkout error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    payment_id = f"pay_{uuid.uuid4().hex[:12]}"
    await db.payment_transactions.insert_one({
        "payment_id": payment_id, "session_id": session.id,
        "user_id": current_user.user_id, "amount": amount, "currency": "usd",
        "status": "pending", "payment_status": "pending",
        "metadata": {"package_id": package_id}, "created_at": datetime.now(timezone.utc).isoformat()
    })
    return {"url": session.url, "session_id": session.id}

@api_router.get("/payments/status/{session_id}")
async def check_payment_status(session_id: str, current_user: User = Depends(get_current_user)):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    payment = await db.payment_transactions.find_one({"session_id": session_id}, {"_id": 0})
    if payment and payment["payment_status"] != session.payment_status:
        await db.payment_transactions.update_one(
            {"session_id": session_id},
            {"$set": {"payment_status": session.payment_status, "status": session.status}}
        )
    return {"session_id": session.id, "status": session.status, "payment_status": session.payment_status}

@api_router.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("Stripe-Signature", "")

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(body, signature, STRIPE_WEBHOOK_SECRET)
        else:
            import json
            event = stripe.Event.construct_from(json.loads(body), stripe.api_key)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        await db.payment_transactions.update_one(
            {"session_id": session["id"]},
            {"$set": {"payment_status": session.get("payment_status", "paid"), "status": "completed"}}
        )
    return {"status": "success"}

@api_router.post("/checkout/create-payment-intent")
async def create_payment_intent(request: PaymentIntentRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price_data": {"currency": "usd", "product_data": {"name": "Playbeat Order"}, "unit_amount": int(request.amount)}, "quantity": 1}],
            mode="payment",
            success_url=f"{FRONTEND_URL}/checkout/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/checkout/cancel",
            metadata={"source": "playbeat_checkout"}
        )
    except Exception as e:
        logger.error(f"Payment intent error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    payment_id = f"pay_{uuid.uuid4().hex[:12]}"
    await db.payment_transactions.insert_one({
        "payment_id": payment_id, "session_id": session.id,
        "amount": request.amount / 100, "currency": "usd",
        "status": "pending", "payment_status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return {"client_secret": session.id, "url": session.url}

@api_router.post("/checkout/confirm-payment")
async def confirm_payment(request: ConfirmPaymentRequest):
    try:
        session = stripe.checkout.Session.retrieve(request.client_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    await db.payment_transactions.update_one(
        {"session_id": request.client_secret},
        {"$set": {"payment_status": session.payment_status, "status": session.status}}
    )
    return {"payment_intent_id": request.client_secret, "status": session.payment_status}


# ── Cart ──────────────────────────────────────────────────────────────────────

@api_router.get("/cart")
async def get_cart(authorization: Optional[str] = Header(None)):
    try:
        if authorization:
            user = await get_current_user(authorization, None)
            cart = await db.carts.find_one({"user_id": user.user_id}, {"_id": 0})
            if cart:
                return {"items": cart.get("items", [])}
    except:
        pass
    return {"items": []}

@api_router.post("/cart")
async def add_to_cart(item: CartItem, authorization: Optional[str] = Header(None)):
    try:
        if authorization:
            user = await get_current_user(authorization, None)
            existing = await db.carts.find_one({"user_id": user.user_id})
            if existing:
                items = existing.get("items", [])
                found = False
                for ci in items:
                    if ci["product_id"] == item.product_id:
                        ci["quantity"] += item.quantity
                        found = True
                        break
                if not found:
                    items.append(item.model_dump())
                await db.carts.update_one({"user_id": user.user_id}, {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}})
            else:
                await db.carts.insert_one({"user_id": user.user_id, "items": [item.model_dump()], "created_at": datetime.now(timezone.utc).isoformat(), "updated_at": datetime.now(timezone.utc).isoformat()})
            return {"message": "Item added to cart"}
        return {"message": "Unauthorized"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@api_router.delete("/cart/{product_id}")
async def remove_from_cart(product_id: str, authorization: Optional[str] = Header(None)):
    try:
        if authorization:
            user = await get_current_user(authorization, None)
            cart = await db.carts.find_one({"user_id": user.user_id})
            if cart:
                items = [i for i in cart.get("items", []) if i["product_id"] != product_id]
                await db.carts.update_one({"user_id": user.user_id}, {"$set": {"items": items, "updated_at": datetime.now(timezone.utc).isoformat()}})
            return {"message": "Item removed from cart"}
        return {"message": "Unauthorized"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Orders from checkout ──────────────────────────────────────────────────────

@api_router.post("/orders/create")
async def create_order_from_checkout(order: OrderCreate, authorization: Optional[str] = Header(None)):
    try:
        order_id = f"ord_{uuid.uuid4().hex[:12]}"
        user_id = None
        if authorization:
            try:
                user = await get_current_user(authorization, None)
                user_id = user.user_id
            except:
                pass

        await db.orders.insert_one({
            "order_id": order_id, "user_id": user_id, "customer_id": user_id,
            "product_id": order.items[0].get("product_id", "multiple") if order.items else "unknown",
            "items": order.items, "amount": order.total,
            "status": "completed", "payment_status": "paid",
            "transaction_id": order.payment_intent_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        if user_id:
            await db.carts.delete_one({"user_id": user_id})
        return {"order_id": order_id, "status": "success"}
    except Exception as e:
        logger.error(f"Order creation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ── Health check ──────────────────────────────────────────────────────────────

@api_router.get("/health")
async def health():
    return {"status": "ok", "app": APP_NAME}


# ── App setup ─────────────────────────────────────────────────────────────────

app.include_router(api_router)

cors_origins = os.environ.get('CORS_ORIGINS', '*')
cors_origins = ['*'] if cors_origins == '*' else cors_origins.split(',')

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True if cors_origins != ['*'] else False,
    allow_origins=cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
