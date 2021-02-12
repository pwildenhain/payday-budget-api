import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel

class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"


class TransactionBase(BaseModel):
    date: datetime.datetime
    name: str
    comment: str
    transaction_type: TransactionType
    amount: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    name: str
    category: str
    budgeted_amount: int
    current_balance: int


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    #transactions: List[Transaction]

    class Config:
        orm_mode = True
