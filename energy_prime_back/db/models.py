"""SQLAlchemy models."""
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    """User create model."""

    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    """User update model."""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserDelete(BaseModel):
    """User delete model."""

    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class TokenData(BaseModel):
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
