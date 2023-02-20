"""Main module for the FastAPI application."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint for the FastAPI application."""
    return {"msg": "Hello World"}


@app.get("/ping")
async def ping() -> dict[str, str]:
    """Ping endpoint for the FastAPI application."""
    return {"ping": "pong"}


def function() -> None:
    """Function docstring."""
    pass
