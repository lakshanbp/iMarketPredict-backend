# app/main.py

from fastapi import FastAPI, Request
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.database import init_db
from app.auth.jwt_bearer import get_current_user_from_token  # 👈 NEW

app = FastAPI(title="iMarketPredict Backend (GraphQL)")

# 👇 Context getter that adds "current_user" from JWT
async def get_context(request: Request):
    try:
        user = await get_current_user_from_token(request)
    except:
        user = None  # Anonymous access if no token or invalid
    return {"current_user": user}

# 👇 Add GraphQL router with context
graphql_app = GraphQLRouter(schema, context_getter=get_context)

# ✅ MongoDB connect
@app.on_event("startup")
async def start_db():
    await init_db()

# ✅ Add GraphQL endpoint
app.include_router(graphql_app, prefix="/graphql")
