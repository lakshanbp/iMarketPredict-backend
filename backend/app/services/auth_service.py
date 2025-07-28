from passlib.context import CryptContext
from app.database import db
from app.models.user_model import UserCreate, UserInDB
from bson.objectid import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔍 Check for existing user
async def get_user_by_email(email: str):
    return await db["users"].find_one({"email": email})

# ✅ Register new user with duplicate check
async def create_user(user: UserCreate):
    existing = await get_user_by_email(user.email)
    if existing:
        raise Exception("⚠️ User already exists with this email")

    hashed = pwd_context.hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed,
        "role": user.role,
    }

    result = await db["users"].insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    return UserInDB(**user_data)

# 🔐 Verify login password
async def verify_password(email: str, plain_password: str):
    user = await get_user_by_email(email)
    if not user:
        return None
    if not pwd_context.verify(plain_password, user["hashed_password"]):
        return None
    return user
