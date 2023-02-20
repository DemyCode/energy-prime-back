"""SQLAlchemy models."""
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None
