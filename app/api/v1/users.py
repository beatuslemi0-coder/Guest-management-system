# app/api/v1/users.py
from datetime import date, datetime, time, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, case, func
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import (
    AdminGuestHousePage,
    AdminGuestHouseResponse,
    AdminGuestHouseSummary,
    AdminGuestPage,
    AdminGuestResponse,
    AdminGuestSummary,
    UserResponse,
    UserStatusUpdate,
)
from app.models.user import User
from app.models.customer import Customer
from app.models.booking import Booking
from app.models.room import Room
from app.api.dependencies import get_current_superuser

router = APIRouter(prefix="/admin/users", tags=["Super Admin Management"])
admin_router = APIRouter(prefix="/admin", tags=["Super Admin Management"])


@admin_router.get("/guest-houses", response_model=AdminGuestHousePage)
def get_guest_houses_for_admin(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_superuser),
):
    room_stats = (
        db.query(
            Room.user_id.label("user_id"),
            func.count(Room.id).label("room_count"),
            func.coalesce(
                func.sum(case((Room.is_available.is_(False), 1), else_=0)),
                0,
            ).label("occupied_room_count"),
            func.coalesce(
                func.sum(case((Room.is_available.is_(True), 1), else_=0)),
                0,
            ).label("available_room_count"),
        )
        .group_by(Room.user_id)
        .subquery()
    )

    today_start = datetime.combine(date.today(), time.min)
    tomorrow_start = today_start + timedelta(days=1)
    booking_stats = (
        db.query(
            Room.user_id.label("user_id"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            and_(
                                Booking.status != "Cancelled",
                                Booking.check_in_date >= today_start,
                                Booking.check_in_date < tomorrow_start,
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("check_ins_today"),
            func.coalesce(
                func.sum(
                    case(
                        (
                            and_(
                                Booking.status != "Cancelled",
                                Booking.check_out_date >= today_start,
                                Booking.check_out_date < tomorrow_start,
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("check_outs_today"),
        )
        .join(Room, Booking.room_id == Room.id)
        .group_by(Room.user_id)
        .subquery()
    )

    businesses = User.is_superuser.is_(False)
    total, room_count, check_ins_today, check_outs_today = (
        db.query(
            func.count(User.id),
            func.coalesce(func.sum(room_stats.c.room_count), 0),
            func.coalesce(func.sum(booking_stats.c.check_ins_today), 0),
            func.coalesce(func.sum(booking_stats.c.check_outs_today), 0),
        )
        .outerjoin(room_stats, room_stats.c.user_id == User.id)
        .outerjoin(booking_stats, booking_stats.c.user_id == User.id)
        .filter(businesses)
        .one()
    )

    rows = (
        db.query(
            User.id,
            User.guesthouse_name,
            User.full_name,
            User.email,
            func.coalesce(room_stats.c.room_count, 0).label("room_count"),
            func.coalesce(room_stats.c.occupied_room_count, 0).label("occupied_room_count"),
            func.coalesce(room_stats.c.available_room_count, 0).label("available_room_count"),
            func.coalesce(booking_stats.c.check_ins_today, 0).label("check_ins_today"),
            func.coalesce(booking_stats.c.check_outs_today, 0).label("check_outs_today"),
        )
        .outerjoin(room_stats, room_stats.c.user_id == User.id)
        .outerjoin(booking_stats, booking_stats.c.user_id == User.id)
        .filter(businesses)
        .order_by(User.created_at.desc(), User.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    guest_houses = [
        AdminGuestHouseResponse(
            id=user_id,
            guesthouse_name=guesthouse_name or owner_name,
            owner_name=owner_name,
            owner_email=owner_email,
            room_count=business_room_count,
            occupied_room_count=occupied_room_count,
            available_room_count=available_room_count,
            check_ins_today=business_check_ins,
            check_outs_today=business_check_outs,
        )
        for (
            user_id,
            guesthouse_name,
            owner_name,
            owner_email,
            business_room_count,
            occupied_room_count,
            available_room_count,
            business_check_ins,
            business_check_outs,
        ) in rows
    ]
    return AdminGuestHousePage(
        total=total,
        skip=skip,
        limit=limit,
        summary=AdminGuestHouseSummary(
            guesthouse_count=total,
            room_count=room_count,
            check_ins_today=check_ins_today,
            check_outs_today=check_outs_today,
        ),
        guest_houses=guest_houses,
    )


# 1. Kuona orodha ya Guest Houses / Users zote (Active & Inactive)
@router.get("/", response_model=List[UserResponse])
def get_all_users_for_admin(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_superuser) # Super Admin Pekee
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@admin_router.get("/guests", response_model=AdminGuestPage)
def get_all_guests_for_admin(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_superuser),
):
    revenue_by_guest = (
        db.query(
            Booking.customer_id.label("customer_id"),
            func.count(Booking.id).label("booking_count"),
            func.coalesce(
                func.sum(
                    case(
                        (Booking.status != "Cancelled", Booking.total_price),
                        else_=0,
                    )
                ),
                0,
            ).label("revenue"),
        )
        .join(Room, Booking.room_id == Room.id)
        .join(
            Customer,
            (Booking.customer_id == Customer.id) & (Room.user_id == Customer.user_id),
        )
        .group_by(Booking.customer_id)
        .subquery()
    )

    guest_count, booking_count, revenue = (
        db.query(
            func.count(Customer.id),
            func.coalesce(func.sum(revenue_by_guest.c.booking_count), 0),
            func.coalesce(func.sum(revenue_by_guest.c.revenue), 0),
        )
        .outerjoin(revenue_by_guest, revenue_by_guest.c.customer_id == Customer.id)
        .one()
    )
    rows = (
        db.query(
            Customer,
            User.full_name.label("business_name"),
            User.email.label("business_email"),
            func.coalesce(revenue_by_guest.c.booking_count, 0).label("booking_count"),
            func.coalesce(revenue_by_guest.c.revenue, 0).label("revenue"),
        )
        .join(User, Customer.user_id == User.id)
        .outerjoin(revenue_by_guest, revenue_by_guest.c.customer_id == Customer.id)
        .order_by(Customer.created_at.desc(), Customer.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    guests = [
        AdminGuestResponse(
            id=customer.id,
            full_name=customer.full_name,
            phone_number=customer.phone_number,
            email=customer.email,
            business_name=business_name,
            business_email=business_email,
            booking_count=guest_booking_count,
            revenue=guest_revenue,
        )
        for customer, business_name, business_email, guest_booking_count, guest_revenue in rows
    ]
    return AdminGuestPage(
        total=guest_count,
        skip=skip,
        limit=limit,
        summary=AdminGuestSummary(
            guest_count=guest_count,
            booking_count=booking_count,
            revenue=revenue,
        ),
        guests=guests,
    )

# 2. Kuweka Guest House kuwa Active au Inactive
@router.put("/{user_id}/status", response_model=UserResponse)
def toggle_user_status(
    user_id: int,
    status_in: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_superuser)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mtumiaji/Guest House haijapatikana!"
        )
    
    user.is_active = status_in.is_active
    db.commit()
    db.refresh(user)
    return user