# app/api/v1/bookings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.repositories.booking_repository import BookingRepository
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/bookings", tags=["Bookings & Check-In Management"])

@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return BookingRepository.create(db=db, booking_in=booking_in)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[BookingResponse])
def list_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return BookingRepository.get_all(db=db, skip=skip, limit=limit)

@router.post("/{booking_id}/checkout", response_model=BookingResponse)
def checkout_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return BookingRepository.checkout(db=db, booking_id=booking_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )