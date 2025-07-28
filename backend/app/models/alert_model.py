from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Alert(BaseModel):
    id: Optional[str] = None
    message: str
    stock_symbol: str
    created_at: datetime
    created_by: str  # user email
