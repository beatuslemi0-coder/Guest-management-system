# app/repositories/booking_repository.py
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.customer import Customer
from app.models.room import Room
from app.schemas.booking import BookingCreate

class BookingRepository:
    @staticmethod
    def get_all(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(Booking)
            .join(Room, Booking.room_id == Room.id)
            .join(Customer, Booking.customer_id == Customer.id)
            .filter(Room.user_id == user_id, Customer.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, booking_in: BookingCreate, user_id: int):
        room = db.query(Room).filter(Room.id == booking_in.room_id, Room.user_id == user_id).first()
        if not room:
            raise ValueError("Chumba hakijapatikana!")

        customer = db.query(Customer).filter(
            Customer.id == booking_in.customer_id,
            Customer.user_id == user_id,
        ).first()
        if not customer:
            raise ValueError("Mteja hakupatikana kwenye biashara yako!")

        if not room.is_available:
            raise ValueError("Samahani, chumba hiki kimeshachukuliwa kwa sasa!")

        delta = booking_in.check_out_date - booking_in.check_in_date
        num_nights = delta.days
        if num_nights <= 0:
            num_nights = 1
        
        total_price = num_nights * room.price_per_night

        db_booking = Booking(
            room_id=booking_in.room_id,
            customer_id=booking_in.customer_id,
            check_in_date=booking_in.check_in_date,
            check_out_date=booking_in.check_out_date,
            total_price=total_price,
            status="Confirmed"
        )

        room.is_available = False

        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        return db_booking
    
    @staticmethod
    def checkout(db: Session, booking_id: int, user_id: int):
        booking = (
            db.query(Booking)
            .join(Room, Booking.room_id == Room.id)
            .join(Customer, Booking.customer_id == Customer.id)
            .filter(
                Booking.id == booking_id,
                Room.user_id == user_id,
                Customer.user_id == user_id,
            )
            .first()
        )
        if not booking:
            raise ValueError("Uhifadhi (Booking) haukupatikana!")
        
        if booking.status == "Completed":
            raise ValueError("Booking hii tayari imeshamalizika (Checked-out)!")

        booking.status = "Completed"

        room = db.query(Room).filter(Room.id == booking.room_id, Room.user_id == user_id).first()
        if room is not None:
            room.is_available = True

        db.commit()
        db.refresh(booking)
        return booking