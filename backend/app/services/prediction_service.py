# app/services/prediction_service.py

from typing import List
from app.models.prediction_model import Prediction
from app.database import db

async def get_all_predictions() -> List[Prediction]:
    cursor = db["predictions"].find().sort("timestamp", -1)
    
    predictions = []
    async for doc in cursor:
        # Replace MongoDB's _id with id as string
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        predictions.append(Prediction(**doc))

    return predictions
