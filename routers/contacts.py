from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from crud import create_contact, delete_object, get_company, get_contact, list_contacts, update_object
from schemas import ContactCreate, ContactResponse, ContactUpdate, ContactStatusUpdate, DaysSinceSentResponse

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact_endpoint(payload: ContactCreate, db: Session = Depends(get_db)):
    """Create a contact belonging to an existing company."""
    if not get_company(db, payload.company_id): raise HTTPException(404, "Company not found")
    return create_contact(db, payload.model_dump())


@router.get("", response_model=list[ContactResponse])
def list_contact_endpoint(company_id: int | None = None, status_filter: str | None = Query(None, alias="status"), db: Session = Depends(get_db)):
    """List contacts, optionally filtered by company ID or status."""
    return list_contacts(db, company_id, status_filter)


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    """Get one contact by ID."""
    obj = get_contact(db, contact_id)
    if not obj: raise HTTPException(404, "Contact not found")
    return obj


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_endpoint(contact_id: int, payload: ContactUpdate, db: Session = Depends(get_db)):
    """Update an existing contact."""
    obj = get_contact(db, contact_id)
    if not obj: raise HTTPException(404, "Contact not found")
    data = payload.model_dump(exclude_unset=True)
    if "company_id" in data and not get_company(db, data["company_id"]): raise HTTPException(404, "Company not found")
    return update_object(db, obj, data)


@router.patch("/{contact_id}/status", response_model=ContactResponse)
def update_contact_status_endpoint(contact_id: int, payload: ContactStatusUpdate, db: Session = Depends(get_db)):
    """Update only a contact's pipeline status after a drag-and-drop action."""
    obj = get_contact(db, contact_id)
    if not obj: raise HTTPException(404, "Contact not found")
    return update_object(db, obj, {"status": payload.status})


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact_endpoint(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact."""
    obj = get_contact(db, contact_id)
    if not obj: raise HTTPException(404, "Contact not found")
    delete_object(db, obj)


@router.get("/{contact_id}/days-since-sent", response_model=DaysSinceSentResponse)
def days_since_sent(contact_id: int, db: Session = Depends(get_db)):
    """Return the number of days since a contact's email was sent."""
    obj = get_contact(db, contact_id)
    if not obj: raise HTTPException(404, "Contact not found")
    return {"contact_id": contact_id, "days_since_sent": (date.today() - obj.date_sent).days if obj.date_sent else None}
