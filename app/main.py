"""Main module for the FastAPI application."""
from pathlib import Path

from fastapi import Depends, FastAPI
from loguru import logger
from sqlmodel import Session, select

from alembic import command
from alembic.config import Config
from app.config import settings
from app.db.db import engine, get_session
from app.db.models import User

app = FastAPI()


@app.on_event("startup")
def alembic_upgrade() -> None:
    """Upgrade the database to the latest version."""
    logger.info("Attempting to upgrade alembic on startup")
    try:
        alembic_ini_path = Path(__file__).parent.parent / "alembic.ini"
        alembic_cfg = Config(str(alembic_ini_path))
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)  # type: ignore
        command.upgrade(alembic_cfg, "head")
        logger.info("Successfully upgraded alembic on startup")
    except Exception:
        logger.exception("Alembic upgrade failed on startup")


@app.get("/", response_model=dict[str, str])
def root() -> dict[str, str]:
    """Root endpoint for the FastAPI application."""
    return {"msg": "Hello World"}


@app.get("/ping", response_model=dict[str, str])
async def ping() -> dict[str, str]:
    """Ping endpoint for the FastAPI application."""
    return {"ping": "pong"}


@app.get("/users", response_model=list[User])
async def get_users(session: Session = Depends(get_session)) -> list[User]:
    """Get all users."""
    heroes = session.exec(select(User)).all()
    return heroes


@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)) -> User:
    """Create a new user."""
    with Session(engine) as session:  # type: ignore
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
