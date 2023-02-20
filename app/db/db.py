"""Database connection and creation of tables."""
from sqlalchemy import create_engine

from app.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("Database not properly configured. Please check your .env file.")

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    isolation_level="REPEATABLE READ",
    # pool_size=settings.DATABASE_POOL_SIZE,
    # max_overflow=settings.DATABASE_MAX_OVERFLOW,
)
