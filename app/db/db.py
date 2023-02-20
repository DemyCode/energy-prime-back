from sqlalchemy import create_engine
from sqlmodel import SQLModel

from app.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
