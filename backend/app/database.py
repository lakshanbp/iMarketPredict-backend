# app/database.py

import motor.motor_asyncio
from app.config import settings

# No tls=True for local MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

db = client[settings.DB_NAME]

async def init_db():
    try:
        # Test a simple command
        await db.command("ping")
        print("✅ MongoDB Connected")
    except Exception as e:
        print("❌ MongoDB Connection Failed:", e)
