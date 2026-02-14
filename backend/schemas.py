from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email_id: str
    street1: str
    address: str
    zipcode7: str
    dob: Optional[datetime] = None