# app/api/v1/rooms.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.room import RoomCreate, RoomUpdate, RoomResponse
from app.repositories.room_repository import RoomRepository
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/rooms", tags=["Rooms Management"])

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(
    room_in: RoomCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_room = RoomRepository.get_by_number(db, room_number=room_in.room_number)
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Namba hii ya chumba tayari ipo kwenye mfumo!"
        )
    return RoomRepository.create(db=db, room_in=room_in)

@router.get("/", response_model=List[RoomResponse])
def list_rooms(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return RoomRepository.get_all(db=db, skip=skip, limit=limit)

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = RoomRepository.get_by_id(db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chumba hakikupatikana!"
        )
    return room

# Endpoint ya Kurekebisha Taarifa au Hali ya Chumba (Update / Status Change)
@router.put("/{room_id}", response_model=RoomResponse)
def update_room(
    room_id: int,
    room_in: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room = RoomRepository.get_by_id(db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chumba kinachotakiwa kurekebisha hakipatikani!"
        )
    return RoomRepository.update(db=db, db_room=room, room_in=room_in)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room = RoomRepository.get_by_id(db, room_id=room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chumba hakikupatikana!"
        )
    RoomRepository.delete(db=db, db_room=room)
    return None