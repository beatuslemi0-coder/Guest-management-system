from datetime import date
import re
from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.report import ReportPeriod, ReportResponse
from app.services.report_service import build_pdf, build_report

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/", response_model=ReportResponse)
def get_report(
    period: ReportPeriod = "monthly",
    reference_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return build_report(db, period, reference_date or date.today(), current_user.id)


@router.get("/pdf")
def download_report_pdf(
    period: ReportPeriod = "monthly",
    reference_date: date | None = None,
    language: Literal["sw", "en"] = "sw",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = build_report(db, period, reference_date or date.today(), current_user.id)
    guesthouse_name = getattr(current_user, "guesthouse_name", None) or current_user.full_name
    filename_prefix = re.sub(r"[^a-zA-Z0-9]+", "-", guesthouse_name).strip("-").lower()
    filename = f"{filename_prefix or 'guest-house'}-ripoti-{report.period}-{report.date_from.isoformat()}.pdf"
    return Response(
        content=build_pdf(report, language, guesthouse_name),
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
