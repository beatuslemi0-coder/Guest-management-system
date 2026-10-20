from collections import defaultdict
from datetime import date, datetime, time, timedelta

from sqlalchemy.orm import Session, joinedload

from app.models.booking import Booking
from app.schemas.report import ReportBooking, ReportPeriod, ReportResponse, ReportSeriesPoint, ReportSummary


def get_period_range(period: ReportPeriod, reference_date: date) -> tuple[date, date]:
    if period == "daily":
        return reference_date, reference_date + timedelta(days=1)

    if period == "weekly":
        start = reference_date - timedelta(days=reference_date.weekday())
        return start, start + timedelta(days=7)

    if period == "monthly":
        start = reference_date.replace(day=1)
        if start.month == 12:
            end = date(start.year + 1, 1, 1)
        else:
            end = date(start.year, start.month + 1, 1)
        return start, end

    start = date(reference_date.year, 1, 1)
    return start, date(reference_date.year + 1, 1, 1)


def _series_dates(period: ReportPeriod, start: date, end: date) -> list[date]:
    if period == "yearly":
        return [date(start.year, month, 1) for month in range(1, 13)]
    return [start + timedelta(days=offset) for offset in range((end - start).days)]


def build_report(db: Session, period: ReportPeriod, reference_date: date) -> ReportResponse:
    start, end = get_period_range(period, reference_date)
    bookings = (
        db.query(Booking)
        .options(joinedload(Booking.room), joinedload(Booking.customer))
        .filter(
            Booking.check_in_date >= datetime.combine(start, time.min),
            Booking.check_in_date < datetime.combine(end, time.min),
        )
        .order_by(Booking.check_in_date, Booking.id)
        .all()
    )

    series_dates = _series_dates(period, start, end)
    counts = defaultdict(int)
    values = defaultdict(float)
    rows = []
    guest_ids = set()
    status_counts = defaultdict(int)

    for booking in bookings:
        bucket = booking.check_in_date.date()
        if period == "yearly":
            bucket = bucket.replace(day=1)
        counts[bucket] += 1
        if booking.status != "Cancelled":
            values[bucket] += booking.total_price
        guest_ids.add(booking.customer_id)
        status_counts[booking.status] += 1
        rows.append(
            ReportBooking(
                id=booking.id,
                guest_name=booking.customer.full_name,
                guest_phone=booking.customer.phone_number,
                room_number=booking.room.room_number,
                room_type=booking.room.room_type,
                check_in_date=booking.check_in_date.date(),
                check_out_date=booking.check_out_date.date(),
                total_price=booking.total_price,
                status=booking.status,
            )
        )

    series = [
        ReportSeriesPoint(
            label=bucket.isoformat() if period != "yearly" else bucket.strftime("%Y-%m"),
            booking_count=counts[bucket],
            booking_value=round(values[bucket], 2),
        )
        for bucket in series_dates
    ]

    return ReportResponse(
        period=period,
        date_from=start,
        date_to=end - timedelta(days=1),
        summary=ReportSummary(
            booking_count=len(bookings),
            guest_count=len(guest_ids),
            booking_value=round(
                sum(booking.total_price for booking in bookings if booking.status != "Cancelled"),
                2,
            ),
            confirmed_count=status_counts["Confirmed"],
            checked_in_count=status_counts["Checked-In"],
            completed_count=status_counts["Completed"],
            cancelled_count=status_counts["Cancelled"],
        ),
        series=series,
        bookings=rows,
    )


def _pdf_text(value: object) -> str:
    text = "".join(character if character.isprintable() else " " for character in str(value))
    text = text.encode("latin-1", "replace").decode("latin-1")
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _draw_text(x: int, y: int, size: int, value: object, color: str = "0.15 0.23 0.23") -> str:
    return f"BT /F1 {size} Tf {color} rg {x} {y} Td ({_pdf_text(value)}) Tj ET\n"


def build_pdf(report: ReportResponse, language: str = "sw") -> bytes:
    rows_per_page = 27
    pages = [report.bookings[index:index + rows_per_page] for index in range(0, len(report.bookings), rows_per_page)]
    if not pages:
        pages = [[]]

    period_names = (
        {
            "daily": "Daily report",
            "weekly": "Weekly report",
            "monthly": "Monthly report",
            "yearly": "Yearly report",
        }
        if language == "en"
        else {
            "daily": "Ripoti ya siku",
            "weekly": "Ripoti ya wiki",
            "monthly": "Ripoti ya mwezi",
            "yearly": "Ripoti ya mwaka",
        }
    )
    page_streams = []

    for page_number, page_rows in enumerate(pages, start=1):
        content = ["q\n0.08 0.48 0.42 rg\n0 770 595 72 re f\nQ\n"]
        title = "NGINAP  |  GUEST HOUSE REPORT" if language == "en" else "NGINAP  |  RIPOTI YA MALAZI"
        content.append(_draw_text(38, 805, 20, title, "1 1 1"))
        content.append(_draw_text(38, 785, 10, f"{period_names[report.period]}: {report.date_from.isoformat()} hadi {report.date_to.isoformat()}", "0.88 0.96 0.94"))

        if page_number == 1:
            if language == "en":
                summary_labels = ("SUMMARY", "Total bookings", "Unique guests", "Reservation value", "Confirmed", "Checked in", "Completed", "Cancelled")
            else:
                summary_labels = ("MUHTASARI", "Jumla ya bookings", "Wageni tofauti", "Thamani ya bookings", "Imethibitishwa", "Amekaa", "Imekamilika", "Imeghairiwa")
            content.append(_draw_text(38, 735, 12, summary_labels[0]))
            content.append(_draw_text(38, 712, 10, f"{summary_labels[1]}: {report.summary.booking_count}"))
            content.append(_draw_text(225, 712, 10, f"{summary_labels[2]}: {report.summary.guest_count}"))
            content.append(_draw_text(390, 712, 10, f"{summary_labels[3]}: {report.summary.booking_value:,.2f}"))
            content.append(_draw_text(38, 693, 9, f"{summary_labels[4]}: {report.summary.confirmed_count}"))
            content.append(_draw_text(180, 693, 9, f"{summary_labels[5]}: {report.summary.checked_in_count}"))
            content.append(_draw_text(285, 693, 9, f"{summary_labels[6]}: {report.summary.completed_count}"))
            content.append(_draw_text(410, 693, 9, f"{summary_labels[7]}: {report.summary.cancelled_count}"))
            header_y = 658
        else:
            header_y = 735

        content.append(f"q\n0.91 0.96 0.94 rg\n34 {header_y - 9} 527 22 re f\nQ\n")
        headers = (
            [(39, "DATE"), (125, "GUEST"), (290, "ROOM"), (365, "STATUS"), (472, "TOTAL")]
            if language == "en"
            else [(39, "TAREHE"), (125, "MGENI"), (290, "CHUMBA"), (365, "HALI"), (472, "JUMLA")]
        )
        for x, label in headers:
            content.append(_draw_text(x, header_y, 8, label, "0.08 0.40 0.35"))

        y = header_y - 27
        for row in page_rows:
            if y < 48:
                break
            content.append(_draw_text(39, y, 8, row.check_in_date.isoformat()))
            content.append(_draw_text(125, y, 8, row.guest_name[:26]))
            content.append(_draw_text(290, y, 8, row.room_number[:12]))
            status = row.status.replace("Checked-In", "Checked in") if language == "en" else row.status
            content.append(_draw_text(365, y, 8, status[:14]))
            content.append(_draw_text(472, y, 8, f"{row.total_price:,.2f}"))
            content.append(f"q\n0.90 0.92 0.92 RG\n38 {y - 6} m 557 {y - 6} l S\nQ\n")
            y -= 21

        if not report.bookings and page_number == 1:
            empty_message = "No bookings in this period." if language == "en" else "Hakuna booking katika kipindi hiki."
            content.append(_draw_text(39, y, 10, empty_message))
        footer = f"Nginap  |  Page {page_number} of {len(pages)}" if language == "en" else f"Nginap  |  Ukurasa {page_number} kati ya {len(pages)}"
        content.append(_draw_text(38, 25, 8, footer, "0.48 0.55 0.55"))
        page_streams.append("".join(content).encode("latin-1"))

    objects: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]
    page_refs = []
    for index, stream in enumerate(page_streams):
        page_id = 4 + index * 2
        stream_id = page_id + 1
        page_refs.append(f"{page_id} 0 R")
        objects.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R >> >> /Contents {stream_id} 0 R >>".encode("ascii")
        )
        objects.append(b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(page_refs)}] /Count {len(page_refs)} >>".encode("ascii")

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_number, body in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_number} 0 obj\n".encode("ascii"))
        pdf.extend(body)
        pdf.extend(b"\nendobj\n")

    xref_offset = len(pdf)
    pdf.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.extend(f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii"))
    return bytes(pdf)
