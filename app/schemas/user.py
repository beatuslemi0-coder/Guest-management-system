# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    guesthouse_name: Optional[str] = None

class UserCreate(UserBase):
    password: str


class GuestHouseNameUpdate(BaseModel):
    guesthouse_name: str = Field(min_length=1, max_length=60)


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class AdminGuestResponse(BaseModel):
    id: int
    full_name: str
    phone_number: str
    email: Optional[str] = None
    business_name: str
    business_email: EmailStr
    booking_count: int
    revenue: float


class AdminGuestSummary(BaseModel):
    guest_count: int
    booking_count: int
    revenue: float


class AdminGuestPage(BaseModel):
    total: int
    skip: int
    limit: int
    summary: AdminGuestSummary
    guests: list[AdminGuestResponse]


class AdminGuestHouseResponse(BaseModel):
    id: int
    guesthouse_name: str
    owner_name: str
    owner_email: EmailStr
    room_count: int
    occupied_room_count: int
    available_room_count: int
    check_ins_today: int
    check_outs_today: int


class AdminGuestHouseSummary(BaseModel):
    guesthouse_count: int
    room_count: int
    check_ins_today: int
    check_outs_today: int


class AdminGuestHousePage(BaseModel):
    total: int
    skip: int
    limit: int
    summary: AdminGuestHouseSummary
    guest_houses: list[AdminGuestHouseResponse]


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    
# Ongeza hizi kwenye app/schemas/user.py
class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str
    
class UserStatusUpdate(BaseModel):
    is_active: bool