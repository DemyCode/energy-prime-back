"""Main module for the FastAPI application."""
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqlmodel import Session, select

from app.db.db import engine
from app.db.models import User

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    """Create database and tables on startup."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


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
    with Session(engine) as session:
        heroes = session.exec(select(User)).all()
        return heroes


@app.post("/users/")
def create_hero(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
