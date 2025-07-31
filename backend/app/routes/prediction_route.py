from fastapi import APIRouter, HTTPException
from app.models.prediction_model import PredictionCreate  # ✅ Pydantic model for input
from app.database import db

router = APIRouter()

@router.post(
    "/api/receive-prediction",
    tags=["📊 Module 2 - Predictions"],
    summary="Receive Prediction from Module 2",
    description="Accepts a prediction payload (signal, confidence, features, explanation) from Module 2 and stores it in MongoDB.",
    response_description="✅ Prediction received and stored successfully"
)
async def receive_prediction(prediction: PredictionCreate):
    """
    Receives prediction data from the ML module (Module 2) and stores it in MongoDB.

    - **ticker**: Stock or index symbol (e.g., ^N225)
    - **timestamp**: ISO formatted datetime string
    - **predicted_signal**: "BUY", "SELL", or "HOLD"
    - **confidence**: Float value indicating model confidence
    - **features**: Dictionary of features used by the model
    - **explanation**: List of most important features with their contribution values
    """
    try:
        pred_dict = prediction.dict()
        await db["predictions"].insert_one(pred_dict)
        return {"message": "✅ Prediction received and stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Failed to store prediction: {str(e)}")
