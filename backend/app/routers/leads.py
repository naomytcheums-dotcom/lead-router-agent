from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_site_password
from app.database import get_db
from app.schemas import LeadIn, RoutedLeadOut
from app.services.lead_runner import LeadRouterError, process_lead, send_notification

router = APIRouter(prefix="/api/leads", tags=["leads"], dependencies=[Depends(require_site_password)])


@router.get("", response_model=list[RoutedLeadOut])
def list_leads(db: Session = Depends(get_db)):
    from app.models import RoutedLead

    return db.query(RoutedLead).order_by(RoutedLead.created_at.desc()).limit(50).all()


@router.post("", response_model=RoutedLeadOut)
def submit_lead(payload: LeadIn, db: Session = Depends(get_db)):
    try:
        lead = process_lead(db, payload.model_dump())
    except LeadRouterError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(502, f"Error analyzing lead: {exc}") from exc
    return lead


@router.post("/{lead_id}/send", response_model=RoutedLeadOut)
async def send(lead_id: int, db: Session = Depends(get_db)):
    try:
        lead = await send_notification(db, lead_id)
    except LeadRouterError as exc:
        raise HTTPException(400, str(exc)) from exc
    return lead
