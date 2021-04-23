from typing import List, Optional
import datetime

from fastapi import APIRouter, Form, Depends
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import Session

from db import schemas
from api.dependencies import get_db
from api.api import add_transaction, get_account, record_payday, update_account

# no prefix here, since we want to redirect the user back to the home page
router = APIRouter()


@router.post(
    "/form/add-transaction", response_class=RedirectResponse, include_in_schema=False
)
def add_transaction_form(
    account_id: int = Form(...),
    amount: int = Form(...),
    comment: Optional[str] = Form(""),
    transaction_type: Optional[str] = Form("debit"),
    db: Session = Depends(get_db),
):

    transaction = schemas.TransactionCreate(
        account_id=account_id,
        amount=amount,
        comment=comment,
        transaction_type=transaction_type,
        date=datetime.datetime.now(),
    )

    add_transaction(transaction, db)

    return RedirectResponse(url="/ui/add-transaction", status_code=HTTP_303_SEE_OTHER)


@router.post(
    "/form/add-income", response_class=RedirectResponse, include_in_schema=False
)
def add_income_form(
    account_id: str = Form(...),
    amount: int = Form(...),
    comment: Optional[str] = Form(""),
    transaction_type: Optional[str] = Form("credit"),
    db: Session = Depends(get_db),
):
    transaction = schemas.TransactionCreate(
        account_id=account_id,
        amount=amount,
        comment=comment,
        transaction_type=transaction_type,
        date=datetime.datetime.now(),
    )

    add_transaction(transaction, db)

    return RedirectResponse(url="/ui", status_code=HTTP_303_SEE_OTHER)


@router.post("/form/transfer", response_class=RedirectResponse, include_in_schema=False)
def transfer_form(
    from_account_id: int = Form(...),
    to_account_id: int = Form(...),
    amount: int = Form(...),
    db: Session = Depends(get_db),
):
    account_withdraw_transaction = schemas.TransactionCreate(
        account_id=from_account_id,
        amount=amount,
        comment=f"Transfer to {from_account_id}",
        transaction_type="debit",
        date=datetime.datetime.now(),
    )

    add_transaction(account_withdraw_transaction, db)

    account_deposit_transaction = schemas.TransactionCreate(
        account_id=to_account_id,
        amount=amount,
        comment=f"Transfer from {to_account_id}",
        transaction_type="credit",
        date=datetime.datetime.now(),
    )

    add_transaction(account_deposit_transaction, db)

    return RedirectResponse(url="/ui", status_code=HTTP_303_SEE_OTHER)


@router.post("/form/payday", response_class=RedirectResponse, include_in_schema=False)
def payday_form(payday: List[schemas.Transaction] = Depends(record_payday)):
    # By adding the record_payday dependency, we're implicitly recording a payday
    return RedirectResponse(url="/ui", status_code=HTTP_303_SEE_OTHER)


@router.post(
    "/form/modify-account", response_class=RedirectResponse, include_in_schema=False
)
def modify_account_form(
    account_id: int = Form(...),
    budgeted_amount: int = Form(...),
    db: Session = Depends(get_db),
):
    account = get_account(account_id, db)
    account.budgeted_amount = budgeted_amount

    update_account(
        account_id,
        schemas.AccountUpdate(
            name=account.name,
            category=account.category,
            budgeted_amount=account.budgeted_amount,
            current_balance=account.current_balance,
        ),
        db,
    )

    return RedirectResponse(url="/ui", status_code=HTTP_303_SEE_OTHER)
