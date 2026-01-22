from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    dob: Optional[datetime] = None
    zipcode: int