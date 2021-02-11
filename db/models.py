from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Account(Base):
    __tablename__ = "budget_summary"

    name = Column(String, primary_key=True, index=True)
    category = Column(String)
    budgeted_amount = Column(Integer)
    current_balance = Column(Integer)

    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transaction_history"

    date = Column(String, primary_key=True)
    name = Column(String, ForeignKey("budget_summary.name"), primary_key=True)
    comment = Column(String)
    transaction_type = Column(String)
    amount = Column(Integer)

    account = relationship("Account", back_populates="transactions")
