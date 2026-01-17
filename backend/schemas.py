from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    zipcode: str
    houseno: Optional[str] = None
    dob: Optional[str] = None
    time: Optional[str] = None
    create_time: datetime = datetime.now()
    update_time: datetime = datetime.now()