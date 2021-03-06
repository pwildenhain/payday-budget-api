from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from . import models, schemas


def get_accounts(db: Session):
    return (
        db.query(models.Account)
        .order_by(models.Account.category, desc(models.Account.budgeted_amount))
        .all()
    )


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        date=transaction.date,
        name=transaction.name,
        transaction_type=transaction.transaction_type,
        comment=transaction.comment,
        amount=transaction.amount,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    # Update account balance to reflect transaction
    update_account_balance(db, db_transaction)
    return db_transaction


def update_account_balance(db: Session, transaction: models.Transaction):
    db_account = (
        db.query(models.Account).filter(models.Account.name == transaction.name).first()
    )
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
