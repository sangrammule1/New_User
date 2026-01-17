from sqlalchemy import Column, Integer, String, Date, Float, Time
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    zipcode = Column(String(10))
    house_number = Column(String(50))
    dob = Column(Date)
    time = Column(Time)
    create_time = Column(Date)
    update_time = Column(Date)