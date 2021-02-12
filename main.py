import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

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
# views
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request, db: Session = Depends(get_db)):
    accounts = get_accounts(db)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "accounts": accounts}
    )

@app.get("/add-transaction", response_class=HTMLResponse, include_in_schema=False)
def add_transaction_view(request: Request):
    return templates.TemplateResponse(
        "add_transaction.html",
        {"request": request}
    )

# endpoints
@app.get("/accounts", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)

@app.post("/transactions", response_model=schemas.Transaction)
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

# forms
@app.post("/add-transaction-form", response_class=RedirectResponse, include_in_schema=False)
def add_transaction_form(
    account_name: str = Form(...),
    amount: int = Form(...),
    comment: Optional[str] = Form(""),
    transaction_type: Optional[str] = Form("debit"),
    date: Optional[datetime.datetime] = Form(datetime.datetime.now()),
    db: Session = Depends(get_db)
):
    transaction = schemas.TransactionCreate(
        name=account_name,
        amount=amount,
        comment=comment,
        transaction_type=transaction_type,
        date=date
    )

    add_transaction(transaction, db)

    return RedirectResponse(url="/add-transaction", status_code=HTTP_303_SEE_OTHER)
