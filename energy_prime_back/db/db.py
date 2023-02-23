"""Database connection and creation of tables."""
from typing import Generator

from sqlalchemy import create_engine
from sqlmodel import Session

from energy_prime_back.config import settings

if settings.DATABASE_URL is None:
    raise ValueError("Database not properly configured. Please check your .env file.")

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    isolation_level="REPEATABLE READ",
    # pool_size=settings.DATABASE_POOL_SIZE,
    # max_overflow=settings.DATABASE_MAX_OVERFLOW,
)


def get_session() -> Generator[Session, None, None]:
    """Get a database session."""
    with Session(engine) as session:  # type: ignore
        yield session
