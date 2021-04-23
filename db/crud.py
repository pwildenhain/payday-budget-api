from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from db import models, schemas

import logging

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO
)


def get_accounts(db: Session):
    return (
        db.query(models.Account)
        .order_by(models.Account.category, desc(models.Account.budgeted_amount))
        .all()
    )


def get_account(db: Session, account_id: int):
    return db.query(models.Account).get(account_id)


def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    # Update account balance to reflect transaction
    update_account_balance(db, db_transaction)
    return db_transaction


def update_account(db: Session, account_id: int, account: schemas.AccountUpdate):
    (
        db.query(models.Account)
        .filter(models.Account.account_id == account_id)
        .update({models.Account.budgeted_amount: account.budgeted_amount})
    )
    db.commit()
    db_account = db.query(models.Account).get(account_id)
    db.refresh(db_account)
    return db_account


def update_account_balance(db: Session, transaction: models.Transaction):
    db_account = transaction.account
    tx_amount = (
        transaction.amount
        if transaction.transaction_type == "credit"
        else -transaction.amount
    )
    new_balance = db_account.current_balance + tx_amount
    db_account.current_balance = new_balance
    db.commit()
    db.refresh(db_account)
    return db_account
