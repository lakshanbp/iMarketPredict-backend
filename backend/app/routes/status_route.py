# app/routes/status_route.py

from fastapi import APIRouter
from datetime import datetime
from app.database import db

router = APIRouter()

@router.get("/api/system/status")
async def get_system_status():
    # Try pinging the database
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    return {
        "status": "healthy",                  # Backend is up
        "database": db_status,               # MongoDB check
        "timestamp": datetime.utcnow().isoformat() + "Z"  # Current UTC time
    }
