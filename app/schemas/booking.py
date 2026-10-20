# app/schemas/booking.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.room import RoomResponse
from app.schemas.customer import CustomerResponse

class BookingCreate(BaseModel):
    room_id: int
    customer_id: int
    check_in_date: datetime
    check_out_date: datetime

class BookingResponse(BaseModel):
    id: int
    room_id: int
    customer_id: int
    check_in_date: datetime
    check_out_date: datetime
    total_price: float
    status: str
    room: Optional[RoomResponse] = None
    customer: Optional[CustomerResponse] = None

    class Config:
        from_attributes = True