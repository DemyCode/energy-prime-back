from fastapi import FastAPI

from app.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {"msg": "Hello World"}


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


@app.get("/db")
def db():
    return {"db": settings.DATABASE_URL}
