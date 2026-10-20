# app/schemas/customer.py
from pydantic import BaseModel
from typing import Optional

class CustomerBase(BaseModel):
    full_name: str
    phone_number: str
    id_number: Optional[str] = None
    email: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    occupation: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    id_number: Optional[str] = None
    email: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    occupation: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        from_attributes = True