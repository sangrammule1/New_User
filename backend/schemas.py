from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    zipcode: int

class User(UserCreate):
    id: int
    create_time: datetime
    update_time: datetime