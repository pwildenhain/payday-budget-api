import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from db import crud, models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import logging

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)


templates = Jinja2Templates(directory="templates")


# endpoints
@app.get("/accounts", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)


@app.post("/transactions", response_model=schemas.Transaction)
def add_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    logging.info(f"add_transaction -- {transaction.amount=}")
    return crud.create_transaction(db, transaction)


@app.post("/payday", response_model=List[schemas.Transaction])
def record_payday(
    db: Session = Depends(get_db),
    accounts: List[schemas.Account] = Depends(get_accounts),
):
    transaction_list = []
    for account in accounts:
        transaction = schemas.TransactionCreate(
            name=account.name,
            amount=account.budgeted_amount,
            comment="payday",
            transaction_type="credit",
            date=datetime.datetime.now(),
        )

        transaction_list += [add_transaction(transaction, db)]

    return transaction_list


# views
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request, accounts: List[schemas.Account] = Depends(get_accounts)):
    return templates.TemplateResponse(
        "index.html", {"request": request, "accounts": accounts}
    )


@app.get("/add-transaction", response_class=HTMLResponse, include_in_schema=False)
def add_transaction_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "add_transaction.html", {"request": request, "accounts": accounts}
    )


@app.get("/add-income", response_class=HTMLResponse, include_in_schema=False)
def add_income_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "add_income.html", {"request": request, "accounts": accounts}
    )


@app.get("/transfer", response_class=HTMLResponse, include_in_schema=False)
def transfer_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "transfer.html", {"request": request, "accounts": accounts}
    )


@app.get("/record-payday", response_class=HTMLResponse, include_in_schema=False)
def record_payday_view(request: Request):
    return templates.TemplateResponse("record_payday.html", {"request": request})


# forms/redirect
@app.post(
    "/add-transaction-form", response_class=RedirectResponse, include_in_schema=False
)
def add_transaction_form(
    account_name: str = Form(...),
    amount: int = Form(...),
    comment: Optional[str] = Form(""),
    transaction_type: Optional[str] = Form("debit"),
    date: Optional[datetime.datetime] = Form(datetime.datetime.now()),
    db: Session = Depends(get_db),
):
    logging.info(f"add_transaction_form -- {amount=}")
    transaction = schemas.TransactionCreate(
        name=account_name,
        amount=amount,
        comment=comment,
        transaction_type=transaction_type,
        date=date,
    )
    logging.info(f"add_transaction_form -- {transaction.amount=}")
    add_transaction(transaction, db)

    return RedirectResponse(url="/add-transaction", status_code=HTTP_303_SEE_OTHER)


@app.post("/add-income-form", response_class=RedirectResponse, include_in_schema=False)
def add_income_form(
    account_name: str = Form(...),
    amount: int = Form(...),
    comment: Optional[str] = Form(""),
    transaction_type: Optional[str] = Form("credit"),
    date: Optional[datetime.datetime] = Form(datetime.datetime.now()),
    db: Session = Depends(get_db),
):
    transaction = schemas.TransactionCreate(
        name=account_name,
        amount=amount,
        comment=comment,
        transaction_type=transaction_type,
        date=date,
    )

    add_transaction(transaction, db)

    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@app.post("/transfer-form", response_class=RedirectResponse, include_in_schema=False)
def transfer_form(
    from_account: str = Form(...),
    to_account: str = Form(...),
    amount: int = Form(...),
    date: Optional[datetime.datetime] = Form(datetime.datetime.now()),
    db: Session = Depends(get_db),
):
    account_withdraw_transaction = schemas.TransactionCreate(
        name=from_account,
        amount=amount,
        comment=f"Transfer to {to_account}",
        transaction_type="debit",
        date=date,
    )

    add_transaction(account_withdraw_transaction, db)

    account_deposit_transaction = schemas.TransactionCreate(
        name=to_account,
        amount=amount,
        comment=f"Transfer from {from_account}",
        transaction_type="credit",
        date=date,
    )

    add_transaction(account_deposit_transaction, db)

    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)


@app.post("/payday-redirect", response_class=RedirectResponse, include_in_schema=False)
def payday_form(payday: List[schemas.Transaction] = Depends(record_payday)):
    # By adding the record_payday dependency, we're implicitly recording a payday
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
