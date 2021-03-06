from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from . import models, schemas

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


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    logging.info(f"create_transaction -- {transaction.amount=}")
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    #db.refresh(db_transaction)
    # Update account balance to reflect transaction
    logging.info(f"create_transaction -- {db_transaction.amount=}")
    update_account_balance(db, transaction)
    return db_transaction


def update_account_balance(db: Session, transaction: models.Transaction):
    db_account = (
        db.query(models.Account).filter(models.Account.name == transaction.name).first()
    )
    logging.info(f"update_account_balance -- {db_account.current_balance=}")
    logging.info(f"update_account_balance -- {transaction.amount=}")
    tx_amount = (
        transaction.amount
        if transaction.transaction_type == "credit"
        else -transaction.amount
    )
    logging.info(f"update_account_balance -- {tx_amount=}")
    new_balance = db_account.current_balance + tx_amount
    db_account.current_balance = new_balance
    logging.info(f"update_account_balance -- {db_account.current_balance=}")
    db.commit()
    db.refresh(db_account)
    return db_account
