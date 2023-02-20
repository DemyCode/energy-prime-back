"""Main module for the FastAPI application."""
from pathlib import Path

from fastapi import FastAPI
from loguru import logger
from sqlmodel import Session, select

from alembic import command
from alembic.config import Config
from app.config import settings
from app.db.db import engine
from app.db.models import User

app = FastAPI()


@app.on_event("startup")
def alembic_upgrade():
    logger.info("Attempting to upgrade alembic on startup")
    try:
        alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)  # type: ignore
        command.upgrade(alembic_cfg, "head")
        logger.info("Successfully upgraded alembic on startup")
    except Exception:
        logger.exception("Alembic upgrade failed on startup")


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint for the FastAPI application."""
    return {"msg": "Hello World"}


@app.get("/ping")
async def ping() -> dict[str, str]:
    """Ping endpoint for the FastAPI application."""
    return {"ping": "pong"}


@app.get("/users")
async def get_users() -> list[User]:
    """Get all users."""
    with Session(engine) as session:  # type: ignore
        heroes = session.exec(select(User)).all()
        return heroes


@app.post("/users/")
def create_hero(user: User) -> User:
    """Create a new user."""
    with Session(engine) as session:  # type: ignore
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
