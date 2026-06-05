# 💾 MongoDB Atlas - Data Management Guide

## Your MongoDB Atlas Database

**Connection String:**
```
mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority
```

**Database Name:** `playbeat_digital`

**Current Data:**
- ✅ **8 Products** (IPTV, Streaming, Software, Gift Cards)
- ✅ **1 Admin User**
- ✅ **0 Customers** (will grow as users sign up)
- ✅ **0 Orders** (will grow as purchases happen)

---

## 📥 Access Your Data from PC

### Option 1: MongoDB Compass (Recommended GUI)

1. **Download MongoDB Compass:**
   - Visit: https://www.mongodb.com/try/download/compass
   - Download and install for your OS

2. **Connect:**
   - Open Compass
   - Click "New Connection"
   - Paste connection string:
     ```
     mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority
     ```
   - Click "Connect"

3. **View Data:**
   - Select database: `playbeat_digital`
   - Browse collections: `products`, `customers`, `orders`, `users`

### Option 2: MongoDB Shell (CLI)

```bash
# Install MongoDB Shell
# Download from: https://www.mongodb.com/try/download/shell

# Connect
mongosh "mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital"

# View products
db.products.find().pretty()

# Count documents
db.products.count()
db.customers.count()
db.orders.count()
```

---

## 💾 Backup Your Data

### Export Data from MongoDB Atlas

**Using mongodump:**
```bash
# Install MongoDB Database Tools
# Download from: https://www.mongodb.com/try/download/database-tools

# Export all collections
mongodump --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" --out=./backup

# This creates a backup folder with all your data
```

**Export to JSON:**
```bash
# Export products
mongoexport --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" --collection=products --out=products.json --jsonArray

# Export customers
mongoexport --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" --collection=customers --out=customers.json --jsonArray

# Export orders
mongoexport --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" --collection=orders --out=orders.json --jsonArray
```

---

## 📤 Import Data (Restore from Backup)

**Using mongorestore:**
```bash
mongorestore --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" ./backup/playbeat_digital
```

**Import from JSON:**
```bash
mongoimport --uri="mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital" --collection=products --file=products.json --jsonArray
```

---

## 🔄 Add More Products

### Using Python Script:

Save this as `add_products.py`:
```python
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
import asyncio
import uuid

MONGO_URI = "mongodb+srv://playbeatadmin:Playbeat2026@playbeat.fwjmwfo.mongodb.net/playbeat_digital?retryWrites=true&w=majority"

async def add_product(name, description, price, category):
    client = AsyncIOMotorClient(MONGO_URI)
    db = client["playbeat_digital"]
    
    product = {
        "product_id": f"prod_{uuid.uuid4().hex[:12]}",
        "name": name,
        "description": description,
        "price": price,
        "category": category,
        "image_url": "",
        "is_visible": True,
        "product_type": "digital_download",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.products.insert_one(product)
    print(f"✅ Added: {name}")
    client.close()

# Example usage:
asyncio.run(add_product(
    "Disney+ Premium Account",
    "1 Year subscription, 4K streaming",
    29.99,
    "Streaming"
))
```

### Using MongoDB Compass:
1. Open Compass
2. Navigate to `playbeat_digital` → `products`
3. Click "ADD DATA" → "Insert Document"
4. Paste product JSON:
```json
{
  "product_id": "prod_abc123",
  "name": "Your Product Name",
  "description": "Product description",
  "price": 19.99,
  "category": "Category",
  "image_url": "",
  "is_visible": true,
  "product_type": "digital_download",
  "created_at": "2026-01-05T00:00:00Z"
}
```

---

## 📊 Monitor Your Data

### In MongoDB Atlas Dashboard:

1. Go to: https://cloud.mongodb.com
2. Login with: playbeatdigital@gmail.com
3. Click on your cluster: "playbeat"
4. Click "Collections" to browse data
5. Click "Metrics" to see usage stats

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** with credentials to GitHub
2. **Use environment variables** in production
3. **Rotate password** periodically in Atlas
4. **Enable IP Whitelist** if you want to restrict access
5. **Enable backup** in Atlas (Settings → Backup)

---

## 📞 MongoDB Atlas Support

- **Dashboard:** https://cloud.mongodb.com
- **Documentation:** https://docs.mongodb.com/manual/
- **Atlas Docs:** https://docs.atlas.mongodb.com/

---

## ✅ Current Status

Your MongoDB Atlas database is:
- ✅ **Connected** and working
- ✅ **Populated** with 8 products
- ✅ **Configured** for production use
- ✅ **Accessible** from anywhere (0.0.0.0/0)
- ✅ **Ready** for Railway deployment

**No action needed - your database is ready to use!**
