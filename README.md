# Playbeat Digital — Backend

FastAPI backend for Playbeat Digital. Deployed on Render.com.

## Tech Stack
- FastAPI + Uvicorn
- MongoDB (Motor async driver)
- Stripe (native SDK)

## Required Environment Variables (set in Render dashboard)
| Variable | Description |
|---|---|
| MONGO_URL | MongoDB connection string |
| DB_NAME | Database name (e.g. `playbeat`) |
| STRIPE_API_KEY | Your Stripe secret key |
| STRIPE_WEBHOOK_SECRET | Stripe webhook signing secret |
| FRONTEND_URL | Your frontend URL |
| BACKEND_URL | This service's URL on Render |
| CORS_ORIGINS | Comma-separated allowed origins |

## Local Development
```bash
cp .env.example .env
# fill in your values
pip install -r requirements.txt
uvicorn server:app --reload
```
