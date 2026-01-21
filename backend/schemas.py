from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None
    address: Optional[str] = None
    zipcode: Optional[int] = None

class User(UserCreate):
    id: int
    created_at: datetime
    update_time: datetime