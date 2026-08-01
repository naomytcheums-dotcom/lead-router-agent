from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import CompanyProfile, GoogleAccount, RoutedLead, TeamMember
from app.services import gmail_send, google_oauth
from app.services.lead_analyzer import analyze_lead


class LeadRouterError(RuntimeError):
    pass


def process_lead(db: Session, payload: dict) -> RoutedLead:
    profile = db.query(CompanyProfile).first()
    if not profile or not profile.company_name.strip() or not profile.products_and_services.strip():
        raise LeadRouterError("Set up your company profile (name + products/services) before processing leads.")

    team = db.query(TeamMember).all()
    team_directory = [{"name": m.name, "email": m.email, "responsibility": m.responsibility} for m in team]

    analysis = analyze_lead(
        profile.company_name,
        profile.products_and_services,
        team_directory,
        payload["lead_name"],
        payload.get("company_name", ""),
        payload["notes"],
        payload.get("city", ""),
        payload.get("country", ""),
        payload.get("mobile", ""),
    )

    lead = RoutedLead(
        lead_name=payload["lead_name"],
        company_name=payload.get("company_name", ""),
        notes=payload["notes"],
        city=payload.get("city", ""),
        country=payload.get("country", ""),
        mobile=payload.get("mobile", ""),
        source=payload.get("source", "Website"),
        is_valid=analysis["is_valid"],
        invalid_reason=analysis["invalid_reason"],
        recipient_emails=analysis["recipient_emails"],
        email_subject=analysis["email_subject"],
        email_body=analysis["email_body"],
        status="reviewed",
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


async def _valid_access_token(db: Session, account: GoogleAccount) -> str:
    if account.token_expiry > datetime.utcnow() + timedelta(seconds=60):
        return account.access_token

    tokens = await google_oauth.refresh_access_token(account.refresh_token)
    account.access_token = tokens["access_token"]
    account.token_expiry = datetime.utcnow() + timedelta(seconds=tokens.get("expires_in", 3600))
    db.commit()
    return account.access_token


async def send_notification(db: Session, lead_id: int) -> RoutedLead:
    lead = db.get(RoutedLead, lead_id)
    if not lead:
        raise LeadRouterError("Lead not found.")
    if not lead.is_valid:
        raise LeadRouterError("This lead was marked invalid and has no notification to send.")
    if lead.status == "sent":
        return lead
    if not lead.recipient_emails:
        raise LeadRouterError("This lead has no recipient email(s).")

    account = db.query(GoogleAccount).first()
    if not account:
        raise LeadRouterError("Google account is not connected yet.")
    access_token = await _valid_access_token(db, account)

    body_html = lead.email_body.replace("\n", "<br>")

    try:
        await gmail_send.send_notification_email(
            access_token,
            to_addresses=lead.recipient_emails,
            subject=lead.email_subject or f"New lead: {lead.lead_name}",
            body_html=body_html,
        )
        lead.status = "sent"
        lead.sent_at = datetime.utcnow()
    except Exception as exc:  # noqa: BLE001
        lead.status = "failed"
        lead.error_message = f"Error sending: {exc}"

    db.commit()
    db.refresh(lead)
    return lead
