import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import uuid

MONGO_URI = "mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority"

PRODUCTS = [
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "IPTV Premium 12 Months", "description": "Full HD & 4K channels. 10,000+ live channels, VOD included.", "price": 59.99, "category": "IPTV", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "IPTV Standard 6 Months", "description": "5,000+ channels in HD. Perfect for everyday streaming.", "price": 34.99, "category": "IPTV", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Netflix Premium Account", "description": "4K UHD. 4 screens simultaneously.", "price": 24.99, "category": "Streaming", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Spotify Family Plan", "description": "6 accounts, ad-free music, offline downloads.", "price": 14.99, "category": "Streaming", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Microsoft Office 2024", "description": "Genuine license key. Word, Excel, PowerPoint, Outlook.", "price": 49.99, "category": "Software", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Windows 11 Pro Key", "description": "Authentic activation key. Instant digital delivery.", "price": 29.99, "category": "Software", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Amazon Gift Card $25", "description": "Redeemable on Amazon.com. Never expires.", "price": 25.00, "category": "Gift Cards", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
    {"product_id": f"prod_{uuid.uuid4().hex[:12]}", "name": "Steam Wallet $50", "description": "Add funds to your Steam account.", "price": 50.00, "category": "Gift Cards", "image_url": "", "is_visible": True, "product_type": "digital_download", "created_at": datetime.now(timezone.utc).isoformat()},
]

async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["playbeat_digital"]
    
    # Clear existing products
    await db.products.delete_many({})
    print("Cleared existing products")
    
    # Insert new products with proper schema
    await db.products.insert_many(PRODUCTS)
    print(f"✅ Inserted {len(PRODUCTS)} products")
    
    client.close()

asyncio.run(seed())
