from sqlalchemy import case, func
from sqlalchemy.orm import Session

from models import Company, Contact


def create_company(db: Session, data: dict) -> Company:
    obj = Company(**data); db.add(obj); db.commit(); db.refresh(obj); return obj


def get_company(db: Session, company_id: int): return db.get(Company, company_id)


def list_companies(db: Session, tier=None, priority=None, status=None):
    query = db.query(Company)
    if tier: query = query.filter(Company.tier == tier)
    if priority: query = query.filter(Company.priority == priority)
    if status: query = query.filter(Company.status == status)
    return query.order_by(Company.id).all()


def update_object(db: Session, obj, data: dict):
    for key, value in data.items(): setattr(obj, key, value)
    db.commit(); db.refresh(obj); return obj


def delete_object(db: Session, obj): db.delete(obj); db.commit()


def create_contact(db: Session, data: dict) -> Contact:
    obj = Contact(**data); db.add(obj); db.commit(); db.refresh(obj); return obj


def get_contact(db: Session, contact_id: int): return db.get(Contact, contact_id)


def list_contacts(db: Session, company_id=None, status=None):
    query = db.query(Contact)
    if company_id: query = query.filter(Contact.company_id == company_id)
    if status: query = query.filter(Contact.status == status)
    return query.order_by(Contact.id).all()


def tier_stats(db: Session):
    sent_count = func.sum(case((Contact.date_sent.is_not(None), 1), else_=0))
    return (
        db.query(Company.tier, func.count(func.distinct(Company.id)), func.coalesce(sent_count, 0))
        .outerjoin(Contact, Contact.company_id == Company.id)
        .group_by(Company.tier)
        .order_by(Company.tier)
        .all()
    )
