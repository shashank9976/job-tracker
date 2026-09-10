from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import get_db
from crud import create_company, delete_object, get_company, list_companies, update_object
from schemas import CompanyCreate, CompanyResponse, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company_endpoint(payload: CompanyCreate, db: Session = Depends(get_db)):
    """Create and return a company."""
    return create_company(db, payload.model_dump())


@router.get("", response_model=list[CompanyResponse])
def list_company_endpoint(tier: str | None = None, priority: str | None = None, status_filter: str | None = Query(None, alias="status"), db: Session = Depends(get_db)):
    """List companies, optionally filtered by tier, priority, or status."""
    return list_companies(db, tier, priority, status_filter)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_endpoint(company_id: int, db: Session = Depends(get_db)):
    """Get one company by ID."""
    obj = get_company(db, company_id)
    if not obj: raise HTTPException(404, "Company not found")
    return obj


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company_endpoint(company_id: int, payload: CompanyUpdate, db: Session = Depends(get_db)):
    """Update an existing company."""
    obj = get_company(db, company_id)
    if not obj: raise HTTPException(404, "Company not found")
    return update_object(db, obj, payload.model_dump(exclude_unset=True))


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company_endpoint(company_id: int, db: Session = Depends(get_db)):
    """Delete a company and its contacts."""
    obj = get_company(db, company_id)
    if not obj: raise HTTPException(404, "Company not found")
    delete_object(db, obj)
