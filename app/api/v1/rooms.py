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
    existing_room = RoomRepository.get_by_number(
        db,
        room_number=room_in.room_number,
        user_id=current_user.id,
    )
    if existing_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Namba hii ya chumba tayari ipo kwenye mfumo!"
        )
    return RoomRepository.create(db=db, room_in=room_in, user_id=current_user.id)

@router.get("/", response_model=List[RoomResponse])
def list_rooms(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Tunahitaji kujua nani anaomba data
):
    # Anarudishwa vyumba vya mtumiaji huyu pekee
    return RoomRepository.get_all_by_user(db=db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    room = RoomRepository.get_by_id(db, room_id=room_id, user_id=current_user.id)
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
    room = RoomRepository.get_by_id(db, room_id=room_id, user_id=current_user.id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chumba kinachotakiwa kurekebisha hakipatikani!"
        )
    if room_in.room_number:
        existing_room = RoomRepository.get_by_number(
            db,
            room_number=room_in.room_number,
            user_id=current_user.id,
        )
        if existing_room and existing_room.id != room.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Namba hii ya chumba tayari ipo kwenye biashara yako!"
            )
    return RoomRepository.update(db=db, db_room=room, room_in=room_in)

@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room = RoomRepository.get_by_id(db, room_id=room_id, user_id=current_user.id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chumba hakikupatikana!"
        )
    RoomRepository.delete(db=db, db_room=room)
    return None