import os

from sqlmodel import SQLModel, create_engine

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL", "sqlite:///./db/test.db")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
