from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CompanyProfile(Base):
    __tablename__ = "lr_company_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_name: Mapped[str] = mapped_column(String, default="")
    products_and_services: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TeamMember(Base):
    __tablename__ = "lr_team_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, default="")
    email: Mapped[str] = mapped_column(String, default="")
    responsibility: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class GoogleAccount(Base):
    __tablename__ = "lr_google_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String, default="")
    access_token: Mapped[str] = mapped_column(Text, default="")
    refresh_token: Mapped[str] = mapped_column(Text, default="")
    token_expiry: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    connected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class RoutedLead(Base):
    __tablename__ = "lr_leads"

    id: Mapped[int] = mapped_column(primary_key=True)

    lead_name: Mapped[str] = mapped_column(String, default="")
    company_name: Mapped[str] = mapped_column(String, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    city: Mapped[str] = mapped_column(String, default="")
    country: Mapped[str] = mapped_column(String, default="")
    mobile: Mapped[str] = mapped_column(String, default="")
    source: Mapped[str] = mapped_column(String, default="")

    is_valid: Mapped[bool] = mapped_column(Boolean, default=False)
    invalid_reason: Mapped[str] = mapped_column(Text, default="")
    recipient_emails: Mapped[str] = mapped_column(String, default="")
    email_subject: Mapped[str] = mapped_column(String, default="")
    email_body: Mapped[str] = mapped_column(Text, default="")

    status: Mapped[str] = mapped_column(String, default="reviewed")
    error_message: Mapped[str] = mapped_column(Text, default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
