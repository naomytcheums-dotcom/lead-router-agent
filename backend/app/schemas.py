from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompanyProfileIn(BaseModel):
    company_name: str
    products_and_services: str


class CompanyProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_name: str
    products_and_services: str
    updated_at: datetime


class TeamMemberIn(BaseModel):
    name: str
    email: str
    responsibility: str


class TeamMemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    responsibility: str
    created_at: datetime


class GoogleStatusOut(BaseModel):
    connected: bool
    email_address: str = ""
    oauth_configured: bool = False


class LeadIn(BaseModel):
    lead_name: str
    company_name: str = ""
    notes: str
    city: str = ""
    country: str = ""
    mobile: str = ""
    source: str = "Website"


class RoutedLeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_name: str
    company_name: str
    notes: str
    city: str
    country: str
    mobile: str
    source: str
    is_valid: bool
    invalid_reason: str
    recipient_emails: str
    email_subject: str
    email_body: str
    status: str
    error_message: str
    created_at: datetime
    sent_at: datetime | None
