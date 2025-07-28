from pydantic import BaseModel, EmailStr
from typing import Literal, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["Admin", "Analyst", "Viewer"] = "Viewer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    hashed_password: str
    role: str
