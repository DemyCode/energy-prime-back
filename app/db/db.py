"""Database connection and creation of tables."""
from sqlalchemy import create_engine
from sqlmodel import SQLModel

from app.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("Database not properly configured. Please check your .env file.")

engine = create_engine(settings.DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)
