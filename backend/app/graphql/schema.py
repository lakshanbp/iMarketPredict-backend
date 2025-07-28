# app/graphql/schema.py

import strawberry
from strawberry.types import Info
from datetime import datetime
from typing import List, Optional

from app.models.user_model import UserCreate
from app.models.alert_model import Alert
from app.services import auth_service, alert_service
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
    id: str                      # ✅ Added ID
    message: str
    stock_symbol: str
    created_at: datetime
    created_by: str

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

        # 🔮 Fake trend (replace with ML later)
        trend = "UP"
        message = f"📈 Predicted trend for {symbol.upper()} is: {trend}"

        # Save alert to DB
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
        return [AlertType(**alert.dict()) for alert in alerts]

# 📦 Register schema
schema = strawberry.Schema(query=Query, mutation=Mutation)
