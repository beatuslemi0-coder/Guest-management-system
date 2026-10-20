# app/models/room.py
from sqlalchemy import Column, String, Float, Boolean
from app.db.session import Base
from app.models.base import TimestampMixin

class Room(Base, TimestampMixin):
    __tablename__ = "rooms"

    room_number = Column(String, unique=True, index=True, nullable=False)
    room_type = Column(String, nullable=False)  # Mfano: Single, Double, VIP, n.k.
    price_per_night = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    description = Column(String, nullable=True)