# app/schemas/room.py
from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    room_number: str
    room_type: str
    price_per_night: float
    description: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class RoomUpdate(BaseModel):
    room_number: Optional[str] = None
    room_type: Optional[str] = None
    price_per_night: Optional[float] = None
    is_available: Optional[bool] = None
    description: Optional[str] = None

class RoomResponse(RoomBase):
    id: int
    is_available: bool

    class Config:
        from_attributes = True