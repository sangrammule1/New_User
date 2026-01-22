from sqlalchemy import Column, Integer, String, Date, Float, Time, TIMESTAMP
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    dob = Column(Date, nullable=True, unique=False)
    zipcode = Column(Integer)
    email = Column(String(100), nullable=False)
    address = Column(String(255))