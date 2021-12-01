import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import crud, models
from api.dependencies import get_db

router = APIRouter(prefix="/api")

# endpoints
@router.get("/accounts", response_model=List[models.Account])
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_accounts(db)


@router.post("/accounts", response_model=models.Account)
def add_account(account: models.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, account)


@router.get("/accounts/{account_id}", response_model=models.Account)
def get_account(account_id: int, db: Session = Depends(get_db)):
    return crud.get_account(db, account_id)


@router.put("/accounts/{account_id}", response_model=models.Account)
def update_account(
    account_id: int, account: models.AccountUpdate, db: Session = Depends(get_db)
):
    return crud.update_account(db, account_id, account)


@router.delete("/accounts/{account_id}", response_model=models.Account)
def delete_account(account: models.AccountDelete, db: Session = Depends(get_db)):
    return crud.delete_account(db, account)


@router.post("/transactions", response_model=models.Transaction)
def add_transaction(
    transaction: models.TransactionCreate, db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)


@router.post("/payday", response_model=List[models.Transaction])
def record_payday(
    db: Session = Depends(get_db),
    accounts: List[models.Account] = Depends(get_accounts),
):
    transaction_list = []
    for account in accounts:
        transaction = models.TransactionCreate(
            account_id=account.account_id,
            amount=account.budgeted_amount,
            comment="payday",
            transaction_type="credit",
            date=datetime.datetime.now(),
        )

        transaction_list += [add_transaction(transaction, db)]

    return transaction_list
