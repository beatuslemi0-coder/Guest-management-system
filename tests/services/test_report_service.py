from datetime import date

from app.schemas.report import ReportBooking, ReportResponse, ReportSummary
from app.services.report_service import build_pdf, get_period_range


def test_report_period_ranges_cover_calendar_boundaries():
    assert get_period_range("daily", date(2026, 10, 20)) == (
        date(2026, 10, 20),
        date(2026, 10, 21),
    )
    assert get_period_range("weekly", date(2026, 1, 1)) == (
        date(2025, 12, 29),
        date(2026, 1, 5),
    )
    assert get_period_range("monthly", date(2026, 12, 20)) == (
        date(2026, 12, 1),
        date(2027, 1, 1),
    )
    assert get_period_range("yearly", date(2024, 2, 29)) == (
        date(2024, 1, 1),
        date(2025, 1, 1),
    )


def test_pdf_report_is_valid_and_splits_long_reports_across_pages():
    bookings = [
        ReportBooking(
            id=index,
            guest_name=f"Guest {index}",
            guest_phone="555-0000",
            room_number="A1",
            room_type="Deluxe",
            check_in_date=date(2026, 10, 1),
            check_out_date=date(2026, 10, 2),
            total_price=100,
            status="Confirmed",
        )
        for index in range(28)
    ]
    report = ReportResponse(
        period="monthly",
        date_from=date(2026, 10, 1),
        date_to=date(2026, 10, 31),
        summary=ReportSummary(
            booking_count=28,
            guest_count=28,
            booking_value=2800,
            confirmed_count=28,
            checked_in_count=0,
            completed_count=0,
            cancelled_count=0,
        ),
        series=[],
        bookings=bookings,
    )

    pdf = build_pdf(report)
    english_pdf = build_pdf(report, "en")

    assert pdf.startswith(b"%PDF-1.4")
    assert b"/Count 2" in pdf
    assert b"%%EOF" in pdf
    assert b"MUHTASARI" in pdf
    assert b"GUEST HOUSE REPORT" in english_pdf
    assert b"SUMMARY" in english_pdf
