import strawberry
from typing import List
from datetime import datetime
from strawberry.scalars import JSON  # ✅ Correct scalar

# 🍓 User input types
@strawberry.input
class UserInput:
    username: str
    email: str
    password: str
    role: str = "Viewer"

@strawberry.input
class LoginInput:
    email: str
    password: str

# 📊 GraphQL types for Predictions
@strawberry.type
class FeatureImportanceType:
    feature: str
    value: float

@strawberry.type
class ExplanationType:
    feature_importance: List[FeatureImportanceType]

@strawberry.type
class PredictionType:
    id: str
    ticker: str
    timestamp: datetime
    predicted_signal: str
    confidence: float
    features: JSON  # ✅ Correct usage of Strawberry JSON scalar
    explanation: ExplanationType
