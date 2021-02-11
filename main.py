from typing import List

from fastapi import FastAPI, Query, Path, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


templates = Jinja2Templates(directory="templates")

@app.get("/accounts", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)

@app.get("/", response_class=HTMLResponse)
def root(request: Request, db: Session = Depends(get_db)):
    accounts = get_accounts(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "accounts": accounts}
    )

@app.post("/transactions/", response_model=schemas.Transaction)
def add_transaction(transaction: schemas.Transaction, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)
