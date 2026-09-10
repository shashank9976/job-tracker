from datetime import date
from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import PlainTextResponse
from sqlalchemy import inspect, text
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import Company, Contact
from crud import tier_stats
from schemas import SummaryResponse, TierStatsResponse, ReminderResponse
from routers import companies, contacts

app = FastAPI(title="Job Application Tracker API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
app.include_router(companies.router)
app.include_router(contacts.router)


def seed_database():
    """Create tables and add sample records only when the database is empty."""
    Base.metadata.create_all(bind=engine)
    if "followup_threshold_days" not in {c["name"] for c in inspect(engine).get_columns("companies")}:
        with engine.begin() as connection:
            connection.execute(text("ALTER TABLE companies ADD COLUMN followup_threshold_days INTEGER NOT NULL DEFAULT 5"))
    db = SessionLocal()
    try:
        if db.query(Company).count() == 0:
            acme = Company(name="Acme Analytics", tier="A", hq_location="Bengaluru", why_target="Strong data platform team", priority="High", status="Researching", people_found=1)
            orbit = Company(name="Orbit Cloud", tier="B", hq_location="Hyderabad", why_target="Growing cloud engineering group", priority="Medium", status="People Found", people_found=1)
            northstar = Company(name="Northstar Labs", tier="A", hq_location="Remote", why_target="Excellent developer tools product", priority="High", status="Not Started")
            db.add_all([acme, orbit, northstar]); db.flush()
            db.add_all([
                Contact(company_id=acme.id, first_name="Priya", last_name="Shah", role_title="Engineering Manager", status="Emails Sent", date_sent=__import__("datetime").date.today(), hook="Shared interest in analytics tooling"),
                Contact(company_id=orbit.id, first_name="Arjun", last_name="Mehta", role_title="Senior Software Engineer", status="Not Started", hook="Cloud infrastructure experience"),
                Contact(company_id=northstar.id, first_name="Maya", last_name="Chen", role_title="Developer Relations Lead", status="Replied", date_sent=__import__("datetime").date.today(), replied=True, hook="Developer community work"),
            ])
            db.commit()
    finally:
        db.close()


seed_database()


@app.get("/stats/summary", response_model=SummaryResponse, tags=["Analytics"])
def summary_stats(db: Session = Depends(get_db)):
    """Return high-level company, outreach, and reply-rate statistics."""
    total_emails = db.query(Contact).filter(Contact.date_sent.is_not(None)).count()
    replies = db.query(Contact).filter(Contact.replied.is_(True)).count()
    return {"total_companies": db.query(Company).count(), "total_contacts": db.query(Contact).count(), "total_emails_sent": total_emails, "total_replies": replies, "reply_rate": round(replies / total_emails * 100, 1) if total_emails else 0}


@app.get("/stats/by-tier", response_model=list[TierStatsResponse], tags=["Analytics"])
def stats_by_tier(db: Session = Depends(get_db)):
    """Return company count and emails sent grouped by company tier."""
    return [{"tier": tier, "company_count": count, "emails_sent": emails} for tier, count, emails in tier_stats(db)]


def get_reminder_rows(db: Session, threshold: int | None):
    """Build reminder records using each company's threshold or the global fallback."""
    rows = []
    for contact in db.query(Contact).join(Company).order_by(Contact.id).all():
        if contact.date_sent is None or contact.status == "Replied":
            continue
        days = (date.today() - contact.date_sent).days
        company_threshold = contact.company.followup_threshold_days if contact.company.followup_threshold_days is not None else 5
        effective_threshold = threshold if threshold is not None else company_threshold
        if days >= effective_threshold:
            rows.append({"contact_id": contact.id, "company": contact.company.name, "contact_name": f"{contact.first_name} {contact.last_name}", "days_since_sent": days, "threshold_days": effective_threshold})
    return rows


@app.get("/reminders", response_model=list[ReminderResponse], tags=["Reminders"])
def reminders(threshold: int | None = Query(None, ge=0), db: Session = Depends(get_db)):
    """Return unreplied contacts at or beyond the requested follow-up threshold."""
    return get_reminder_rows(db, threshold)


@app.post("/reminders/digest", response_class=PlainTextResponse, tags=["Reminders"])
def reminder_digest(threshold: int | None = Query(None, ge=0), db: Session = Depends(get_db)):
    """Return a plain-text follow-up digest suitable for a future email or Slack webhook."""
    rows = get_reminder_rows(db, threshold)
    if not rows:
        return "Job Application Tracker — Follow-up Digest\n\nNo contacts currently need follow-up."
    lines = ["Job Application Tracker — Follow-up Digest", "", "Contacts needing follow-up:"]
    lines.extend(f"- {row['company']} — {row['contact_name']} — {row['days_since_sent']} days since sent" for row in rows)
    return "\n".join(lines)


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
