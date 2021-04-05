from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from db import models
from db.database import engine

from api import api, forms, views

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.router)
app.include_router(views.router)
app.include_router(forms.router)
