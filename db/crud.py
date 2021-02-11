from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import desc

from . import models, schemas

def get_accounts(db: Session):
    return db.query(models.Account).order_by(models.Account.category, desc(models.Account.budgeted_amount)).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        date=transaction.date,
        name=transaction.name,
        transaction_type=transaction.transaction_type,
        comment=transaction.comment,
        amount=transaction.amount
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    # Update account balance to reflect transaction
    update_account_balance(db, db_transaction.name)
    return db_transaction

def update_account_balance(db: Session, account_name: str):
    account_transactions = db.query(models.Transaction.amount, models.Transaction.transaction_type).filter(models.Transaction.name == account_name).all()
    account_balance = sum([amount if tx_type == "credit" else -amount for amount, tx_type in account_transactions])
    db_account = db.query(models.Account).filter(models.Account.name == account_name).first()
    db_account.current_balance = account_balance
    db.commit()
    db.refresh(db_account)
    return db_account
