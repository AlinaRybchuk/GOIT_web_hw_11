from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import func
from datetime import date, timedelta

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        models.Contact.first_name.ilike(f"%{query}%") |
        models.Contact.last_name.ilike(f"%{query}%") |
        models.Contact.email.ilike(f"%{query}%")
    ).all()

def get_birthday_contacts(db: Session):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birth_date >= today,
        models.Contact.birth_date <= next_week
    ).all()
