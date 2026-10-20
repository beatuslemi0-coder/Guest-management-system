# app/repositories/room_repository.py
from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomUpdate

class RoomRepository:
    @staticmethod
    def get_by_id(db: Session, room_id: int):
        return db.query(Room).filter(Room.id == room_id).first()

    @staticmethod
    def get_by_number(db: Session, room_number: str):
        return db.query(Room).filter(Room.room_number == room_number).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Room).offset(skip).limit(limit).all()

    @staticmethod
    def create(db: Session, room_in: RoomCreate):
        db_room = Room(
            room_number=room_in.room_number,
            room_type=room_in.room_type,
            price_per_night=room_in.price_per_night,
            description=room_in.description,
            is_available=True  # Kikiundwa kwa mara ya kwanza kinakuwa wazi
        )
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def update(db: Session, db_room: Room, room_in: RoomUpdate):
        update_data = room_in.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_room, key, value)
        db.commit()
        db.refresh(db_room)
        return db_room

    @staticmethod
    def delete(db: Session, db_room: Room):
        db.delete(db_room)
        db.commit()
        return db_room