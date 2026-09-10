from datetime import date
from pydantic import BaseModel, ConfigDict, Field

from models import CompanyStatus, Priority


class CompanyBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    tier: str = Field(min_length=1, max_length=50)
    hq_location: str | None = None
    why_target: str | None = None
    linkedin_search_url: str | None = None
    careers_url: str | None = None
    priority: Priority = Priority.MEDIUM
    status: CompanyStatus = CompanyStatus.NOT_STARTED
    people_found: int = Field(default=0, ge=0)
    emails_sent: int = Field(default=0, ge=0)
    followup_threshold_days: int = Field(default=5, ge=0)
    notes: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    tier: str | None = Field(default=None, min_length=1, max_length=50)
    hq_location: str | None = None
    why_target: str | None = None
    linkedin_search_url: str | None = None
    careers_url: str | None = None
    priority: Priority | None = None
    status: CompanyStatus | None = None
    people_found: int | None = Field(default=None, ge=0)
    emails_sent: int | None = Field(default=None, ge=0)
    followup_threshold_days: int | None = Field(default=None, ge=0)
    notes: str | None = None


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ContactBase(BaseModel):
    company_id: int = Field(gt=0)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    role_title: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    email_source: str | None = None
    hook: str | None = None
    status: str = "Not Started"
    date_sent: date | None = None
    opened: bool = False
    replied: bool = False
    followup_sent: bool = False
    outcome: str | None = None
    notes: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    company_id: int | None = Field(default=None, gt=0)
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    role_title: str | None = None
    linkedin_url: str | None = None
    email: str | None = None
    email_source: str | None = None
    hook: str | None = None
    status: str | None = None
    date_sent: date | None = None
    opened: bool | None = None
    replied: bool | None = None
    followup_sent: bool | None = None
    outcome: str | None = None
    notes: str | None = None


class ContactStatusUpdate(BaseModel):
    status: str = Field(min_length=1, max_length=50)


class ContactResponse(ContactBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class DaysSinceSentResponse(BaseModel):
    contact_id: int
    days_since_sent: int | None


class SummaryResponse(BaseModel):
    total_companies: int
    total_contacts: int
    total_emails_sent: int
    total_replies: int
    reply_rate: float


class TierStatsResponse(BaseModel):
    tier: str
    company_count: int
    emails_sent: int


class ReminderResponse(BaseModel):
    contact_id: int
    company: str
    contact_name: str
    days_since_sent: int
    threshold_days: int
