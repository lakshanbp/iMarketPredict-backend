import strawberry
from strawberry.types import Info
from datetime import datetime
from typing import List
from strawberry.scalars import JSON

from app.models.user_model import UserCreate
from app.models.alert_model import Alert
from app.models.prediction_model import Prediction
from app.services import auth_service, alert_service, prediction_service
from app.auth.jwt_handler import create_access_token
from app.graphql.types import UserInput, LoginInput  # GraphQL input types

# 🧾 Response model for login
@strawberry.type
class AuthResponse:
    token: str
    email: str
    role: str

# 📢 Alert GraphQL type
@strawberry.type
class AlertType:
    id: str
    message: str
    stock_symbol: str
    created_at: datetime
    created_by: str

# 📈 FeatureImportance GraphQL type
@strawberry.type
class FeatureImportanceType:
    feature: str
    value: float

# 📈 Explanation GraphQL type
@strawberry.type
class ExplanationType:
    feature_importance: List[FeatureImportanceType]

# 🔮 Prediction GraphQL type
@strawberry.type
class PredictionType:
    id: str
    ticker: str
    timestamp: datetime
    predicted_signal: str
    confidence: float
    features: JSON
    explanation: ExplanationType

# 🔧 All GraphQL mutations
@strawberry.type
class Mutation:

    @strawberry.mutation
    async def register(self, user_input: UserInput) -> str:
        user = await auth_service.create_user(UserCreate(**user_input.__dict__))
        return f"✅ User {user.email} registered!"

    @strawberry.mutation
    async def login(self, login_input: LoginInput) -> AuthResponse:
        user = await auth_service.verify_password(login_input.email, login_input.password)
        if not user:
            raise Exception("❌ Invalid credentials")
        token = create_access_token({"sub": user["email"], "role": user["role"]})
        return AuthResponse(token=token, email=user["email"], role=user["role"])

    @strawberry.mutation
    async def predictStockTrend(self, info: Info, symbol: str) -> str:
        user = info.context.get("current_user")
        if not user or user["role"] not in ["Admin", "Analyst"]:
            raise Exception("🚫 Only Admin or Analyst can request predictions")

        trend = "UP"  # 🚧 Replace with real ML model output
        message = f"📈 Predicted trend for {symbol.upper()} is: {trend}"

        await alert_service.create_alert(message, symbol.upper(), user["email"])
        return message

# 📊 All GraphQL queries
@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello from iMarketPredict GraphQL!"

    @strawberry.field
    def whoami(self, info: Info) -> str:
        user = info.context.get("current_user")
        if not user:
            raise Exception("❌ Unauthorized")
        return f"👤 Logged in as {user['email']} with role: {user['role']}"

    @strawberry.field
    def adminOnly(self, info: Info) -> str:
        user = info.context.get("current_user")
        if not user or user["role"] != "Admin":
            raise Exception("🚫 Admin access only")
        return "✅ Welcome, Admin! You have full access."

    @strawberry.field
    async def getAlerts(self, info: Info) -> List[AlertType]:
        user = info.context.get("current_user")
        if not user:
            raise Exception("❌ Unauthorized")
        alerts = await alert_service.get_all_alerts()
        return [AlertType(
            id=alert.id,
            message=alert.message,
            stock_symbol=alert.stock_symbol,
            created_at=alert.created_at,
            created_by=alert.created_by
        ) for alert in alerts]

    @strawberry.field
    async def getPredictions(self, info: Info) -> List[PredictionType]:
        user = info.context.get("current_user")
        if not user:
            raise Exception("❌ Unauthorized")
        predictions = await prediction_service.get_all_predictions()
        return [PredictionType(
            id=p.id,
            ticker=p.ticker,
            timestamp=p.timestamp,
            predicted_signal=p.predicted_signal,
            confidence=p.confidence,
            features=p.features,
            explanation=ExplanationType(
                feature_importance=[
                    FeatureImportanceType(feature=fi.feature, value=fi.value)
                    for fi in p.explanation.feature_importance
                ]
            )
        ) for p in predictions]

# 📦 Register schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
