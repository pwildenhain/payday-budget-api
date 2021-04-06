from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from db import models
from db.database import engine

from api import api, forms, views

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(views.router.prefix)

app.include_router(api.router)
app.include_router(views.router)
app.include_router(forms.router)
