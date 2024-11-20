from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, db

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)

def get_db():
    db = db.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main_root():
    return {"message": "Application V0.0.1"}

@app.post("/contacts/", response_model=schemas.Contact)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db=db, contact=contact)

@app.get("/contacts/", response_model=list[schemas.Contact])
def get_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_contacts(db=db, skip=skip, limit=limit)

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = crud.delete_contact(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=list[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)

@app.get("/contacts/birthday/", response_model=list[schemas.Contact])
def get_birthday_contacts(db: Session = Depends(get_db)):
    return crud.get_birthday_contacts(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)