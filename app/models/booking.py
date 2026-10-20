# app/models/booking.py
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.base import TimestampMixin

class Booking(Base, TimestampMixin):
    __tablename__ = "bookings"

    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    
    check_in_date = Column(DateTime, nullable=False)
    check_out_date = Column(DateTime, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Confirmed") # Confirmed, Checked-In, Cancelled, Completed

    # Mahusiano na Tables zingine
    room = relationship("Room")
    customer = relationship("Customer")