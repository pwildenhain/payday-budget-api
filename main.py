from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from db.database import create_db_and_tables

from api import api, forms, views

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return RedirectResponse(views.router.prefix)


app.include_router(api.router)
app.include_router(views.router)
app.include_router(forms.router)
