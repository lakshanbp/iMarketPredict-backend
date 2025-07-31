# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.graphql.schema import schema
from app.database import init_db
from app.auth.jwt_bearer import get_current_user_from_token
from app.routes.prediction_route import router as prediction_router  # ✅ Module 2 REST route
from app.routes.status_route import router as status_router          # ✅ System health check route

# ✅ API metadata for Swagger & ReDoc
app = FastAPI(
    title="iMarketPredict Backend (GraphQL + REST)",
    description="""
    This backend service supports iMarketPredict with:
    
    • 📈 REST API to receive predictions from Module 2  
    • 📊 GraphQL API to retrieve predictions, alerts, and manage access  
    • 🔐 JWT Auth with role-based context  
    • 🧠 MongoDB integration and modular architecture  
    """,
    version="0.1.0",
    contact={
        "name": "Lasith (Module 3 Developer)",
        "email": "your.email@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "📊 Module 2 - Predictions",
            "description": "Endpoints for ML predictions (received via POST from Module 2)"
        },
        {
            "name": "🧪 GraphQL API",
            "description": "All queries and mutations related to predictions, alerts, and authentication"
        },
        {
            "name": "📡 System Status",
            "description": "Health check and backend status monitoring"
        }
    ]
)

# ✅ Enable CORS for frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Add user context for GraphQL
async def get_context(request: Request):
    try:
        user = await get_current_user_from_token(request)
    except:
        user = None
    return {"current_user": user}

# ✅ Mount GraphQL API with context
graphql_app = GraphQLRouter(schema, context_getter=get_context)

# ✅ MongoDB connection on startup
@app.on_event("startup")
async def start_db():
    await init_db()

# ✅ Include REST API routes
app.include_router(prediction_router, tags=["📊 Module 2 - Predictions"])
app.include_router(status_router, tags=["📡 System Status"])

# ✅ GraphQL route
app.include_router(graphql_app, prefix="/graphql")
