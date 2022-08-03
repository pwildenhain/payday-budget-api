from typing import List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import schemas
from api.api import get_accounts

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/ui")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def root(request: Request, accounts: List[schemas.Account] = Depends(get_accounts)):
    budget_total = sum([account.budgeted_amount for account in accounts])
    balance_total = sum([account.current_balance for account in accounts])

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "accounts": accounts,
            "budget_total": budget_total,
            "balance_total": balance_total,
        },
    )


@router.get("/add-transaction", response_class=HTMLResponse, include_in_schema=False)
def add_transaction_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "add_transaction.html", {"request": request, "accounts": accounts}
    )


@router.get("/add-income", response_class=HTMLResponse, include_in_schema=False)
def add_income_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "add_income.html", {"request": request, "accounts": accounts}
    )


@router.get("/transfer", response_class=HTMLResponse, include_in_schema=False)
def transfer_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "transfer.html", {"request": request, "accounts": accounts}
    )


@router.get("/record-payday", response_class=HTMLResponse, include_in_schema=False)
def record_payday_view(request: Request):
    return templates.TemplateResponse("record_payday.html", {"request": request})


@router.get("/modify/update-account", response_class=HTMLResponse, include_in_schema=False)
def update_account_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "update_account.html", {"request": request, "accounts": accounts}
    )

@router.get("/modify/create-account", response_class=HTMLResponse, include_in_schema=False)
def create_account_view(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})


@router.get("/modify/delete-account", response_class=HTMLResponse, include_in_schema=False)
def delete_account_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "delete_account.html", {"request": request, "accounts": accounts}
    )
