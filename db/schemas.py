import datetime
from enum import Enum

from pydantic import BaseModel


class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"


class TransactionBase(BaseModel):
    date: datetime.datetime
    account_id: int
    comment: str
    transaction_type: TransactionType
    amount: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    transaction_id: int
    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    name: str
    category: str
    budgeted_amount: int
    current_balance: int


class AccountCreate(AccountBase):
    pass

    class Config:
        orm_mode = True


class AccountUpdate(AccountBase):
    pass

    class Config:
        orm_mode = True


class AccountDelete(BaseModel):
    account_id: int

    class Config:
        orm_mode = True


class Account(AccountBase):
    account_id: int

    class Config:
        orm_mode = True
