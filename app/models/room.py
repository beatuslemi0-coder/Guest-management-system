# app/models/room.py
from sqlalchemy import Column, String, Float, Boolean, Integer, ForeignKey, UniqueConstraint
from app.db.session import Base
from app.models.base import TimestampMixin

class Room(Base, TimestampMixin):
    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint("user_id", "room_number", name="uq_rooms_user_room_number"),
    )

    room_number = Column(String, index=True, nullable=False)
    room_type = Column(String, nullable=False)  # Mfano: Single, Double, VIP, n.k.
    price_per_night = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)