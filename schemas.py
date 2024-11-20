from pydantic import BaseModel
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    birth_date: Optional[date] = None
    additional_info: Optional[str] = None

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True
