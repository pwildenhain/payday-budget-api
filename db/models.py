from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    category = Column(String)
    budgeted_amount = Column(Integer)
    current_balance = Column(Integer)

    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.account_id"))
    comment = Column(String)
    transaction_type = Column(String)
    amount = Column(Integer)

    account = relationship("Account", back_populates="transactions")
