from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class AccountBase(SQLModel):
    name: str
    category: str
    budgeted_amount: int
    current_balance: int


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    account_id: int


class AccountDelete(AccountBase):
    account_id: int


class AccountRead(AccountBase):
    account_id: int


class Account(AccountBase, table=True):
    __tablename__ = "accounts"

    account_id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(back_populates="account")


class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"


class TransactionBase(SQLModel):
    date: datetime
    account_id: int = Field(default=None, foreign_key="accounts.account_id")
    transaction_type: TransactionType
    amount: int
    comment: Optional[str]


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase, table=True):

    __tablename__ = "transactions"

    transaction_id: Optional[int] = Field(default=None, primary_key=True)

    account: Optional[Account] = Relationship(back_populates="transactions")
