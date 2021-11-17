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
    return templates.TemplateResponse(
        "index.html", {"request": request, "accounts": accounts}
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


@router.get("/update-account", response_class=HTMLResponse, include_in_schema=False)
def update_account_view(
    request: Request, accounts: List[schemas.Account] = Depends(get_accounts)
):
    return templates.TemplateResponse(
        "update_account.html", {"request": request, "accounts": accounts}
    )

@router.get("/create-account", response_class=HTMLResponse, include_in_schema=False)
def create_account_view(request: Request):
    return templates.TemplateResponse("create_account.html", {"request": request})
