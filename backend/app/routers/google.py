from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.auth import require_site_password
from app.config import settings
from app.database import get_db
from app.models import GoogleAccount
from app.schemas import GoogleStatusOut
from app.services import google_oauth

router = APIRouter(prefix="/api/google", tags=["google"])


@router.get("/connect")
def connect():
    if not settings.google_client_id:
        raise HTTPException(400, "Google OAuth is not configured on this server.")
    return RedirectResponse(google_oauth.build_auth_url())


@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db)):
    tokens = await google_oauth.exchange_code(code)
    email_address = await google_oauth.get_user_email(tokens["access_token"])

    account = db.query(GoogleAccount).first()
    if not account:
        account = GoogleAccount()
        db.add(account)

    account.email_address = email_address
    account.access_token = tokens["access_token"]
    if tokens.get("refresh_token"):
        account.refresh_token = tokens["refresh_token"]
    account.token_expiry = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    account.connected_at = datetime.utcnow()
    db.commit()

    return RedirectResponse(f"{settings.frontend_url}?connected=true")


@router.get("/status", response_model=GoogleStatusOut, dependencies=[Depends(require_site_password)])
def status(db: Session = Depends(get_db)):
    oauth_configured = bool(settings.google_client_id and settings.google_client_secret)
    account = db.query(GoogleAccount).first()
    if not account or not account.refresh_token:
        return GoogleStatusOut(connected=False, oauth_configured=oauth_configured)
    return GoogleStatusOut(connected=True, email_address=account.email_address, oauth_configured=oauth_configured)
