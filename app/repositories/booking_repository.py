# app/repositories/booking_repository.py
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.room import Room
from app.schemas.booking import BookingCreate

class BookingRepository:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Booking).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, booking_in: BookingCreate):
        # 1. Pata chumba ili ujue bei yake kwa usiku
        room = db.query(Room).filter(Room.id == booking_in.room_id).first()
        if not room:
            raise ValueError("Chumba hakijapatikana!")

        # 2. Hakikisha chumba kiko wazi
        if not room.is_available:
            raise ValueError("Samahani, chumba hiki kimeshachukuliwa kwa sasa!")

        # 3. Hesabu idadi ya siku na bei ya jumla
        delta = booking_in.check_out_date - booking_in.check_in_date
        num_nights = delta.days
        if num_nights <= 0:
            num_nights = 1  # Kima cha chini ni siku 1
        
        total_price = num_nights * room.price_per_night

        # 4. Tengeneza booking mpya
        db_booking = Booking(
            room_id=booking_in.room_id,
            customer_id=booking_in.customer_id,
            check_in_date=booking_in.check_in_date,
            check_out_date=booking_in.check_out_date,
            total_price=total_price,
            status="Confirmed"
        )

        # 5. Badilisha hali ya chumba kuwa kimechukuliwa (is_available = False)
        room.is_available = False

        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    
    @staticmethod
    def checkout(db: Session, booking_id: int):
        # 1. Tafuta booking husika
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise ValueError("Uhifadhi (Booking) haukupatikana!")
        
        if booking.status == "Completed":
            raise ValueError("Booking hii tayari imeshamalizika (Checked-out)!")

        # 2. Badilisha status ya booking iwe Completed
        booking.status = "Completed"

        # 3. Tafuta chumba kilichohusika na ukirudishe kuwa wazi (is_available = True)
        room = db.query(Room).filter(Room.id == booking.room_id).first()
        if room:
            room.is_available = True

        db.commit()
        db.refresh(booking)
        return booking