# app/models/customer.py
from sqlalchemy import Column, String
from app.db.session import Base
from app.models.base import TimestampMixin

class Customer(Base, TimestampMixin):
    __tablename__ = "customers"

    full_name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    id_number = Column(String, unique=True, nullable=True) # Namba ya Kitambulisho / Leseni / NIDA
    email = Column(String, nullable=True)
    
    # Taarifa za ziada za usalama na ufuatiliaji
    origin = Column(String, nullable=True)      
    destination = Column(String, nullable=True)
    occupation = Column(String, nullable=True)