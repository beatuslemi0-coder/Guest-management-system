from datetime import date
from typing import Literal

from pydantic import BaseModel


ReportPeriod = Literal["daily", "weekly", "monthly", "yearly"]


class ReportSummary(BaseModel):
    booking_count: int
    guest_count: int
    booking_value: float
    confirmed_count: int
    checked_in_count: int
    completed_count: int
    cancelled_count: int


class ReportSeriesPoint(BaseModel):
    label: str
    booking_count: int
    booking_value: float


class ReportBooking(BaseModel):
    id: int
    guest_name: str
    guest_phone: str
    room_number: str
    room_type: str
    check_in_date: date
    check_out_date: date
    total_price: float
    status: str


class ReportResponse(BaseModel):
    period: ReportPeriod
    date_from: date
    date_to: date
    summary: ReportSummary
    series: list[ReportSeriesPoint]
    bookings: list[ReportBooking]
