from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class FeatureImportance(BaseModel):
    feature: str
    value: float

class Explanation(BaseModel):
    feature_importance: List[FeatureImportance]

# Used when receiving data from Module 2
class PredictionCreate(BaseModel):
    ticker: str
    timestamp: datetime
    predicted_signal: str
    confidence: float
    features: Dict[str, float]
    explanation: Explanation

# Used when returning predictions to frontend or GraphQL
class Prediction(PredictionCreate):
    id: str  # Only added when retrieved from DB
