import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import crud, schemas
from api.dependencies import get_db

router = APIRouter(prefix="/api")

# endpoints
@router.get("/accounts", response_model=List[schemas.Account])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)


@router.post("/accounts", response_model=schemas.Account)
def add_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, account)


@router.get("/accounts/{account_id}", response_model=schemas.Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return crud.get_account(db, account_id)


@router.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, account: schemas.AccountUpdate, db: Session = Depends(get_db)):
    return crud.update_account(db, account_id, account)


@router.delete("/accounts/{account_id}", response_model=schemas.Account)
def delete_account(account: schemas.AccountDelete, db: Session = Depends(get_db)):
    return crud.delete_account(db, account)


@router.post("/transactions", response_model=schemas.Transaction)
def add_transaction(
    transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)


@router.post("/payday", response_model=List[schemas.Transaction])
def record_payday(
    db: Session = Depends(get_db),
    accounts: List[schemas.Account] = Depends(get_accounts),
):
    transaction_list = []
    for account in accounts:
        transaction = schemas.TransactionCreate(
            account_id=account.account_id,
            amount=account.budgeted_amount,
            comment="payday",
            transaction_type="credit",
            date=datetime.datetime.now(),
        )

        transaction_list += [add_transaction(transaction, db)]

    return transaction_list
