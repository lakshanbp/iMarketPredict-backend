from datetime import datetime
from app.models.alert_model import Alert
from app.database import db

async def create_alert(message: str, stock_symbol: str, created_by: str):
    alert_data = {
        "message": message,
        "stock_symbol": stock_symbol,
        "created_at": datetime.utcnow(),
        "created_by": created_by
    }
    result = await db["alerts"].insert_one(alert_data)
    alert_data["id"] = str(result.inserted_id)
    return Alert(**alert_data)

async def get_all_alerts():
    cursor = db["alerts"].find().sort("created_at", -1)
    return [Alert(**{**doc, "id": str(doc["_id"])}) async for doc in cursor]
