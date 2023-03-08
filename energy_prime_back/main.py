"""Main module for the FastAPI application."""
from datetime import datetime, timedelta
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from loguru import logger
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, select

from energy_prime_back.config import settings
from energy_prime_back.db.db import engine, get_session
from energy_prime_back.db.models import Token, TokenData, User, UserCreate

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

if settings.ALCHEMY_UPGRADE:

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


if settings.CREATE_TABLES:
    SQLModel.metadata.create_all(engine)


@app.get("/", response_model=dict[str, str])
def root() -> dict[str, str]:
    """Root endpoint for the FastAPI application."""
    return {"msg": "Hello World"}


@app.get("/ping", response_model=dict[str, str])
async def ping() -> dict[str, str]:
    """Ping endpoint for the FastAPI application."""
    return {"ping": "pong"}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user(session: Session, username: str) -> User | None:
    user = session.exec(select(User).where(User.username == username)).first()
    if user is not None:
        return User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
    return None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session, username: str, password: str):
    user = get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)
) -> dict[str, str]:
    user = authenticate_user(session, form_data.username, form_data.password)
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None and not isinstance(username, str):
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == token_data.username)).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> User:
    """Create a new user."""
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
        is_active=True,
        is_superuser=False,
    )
    session.add(new_user)
    session.commit()
    return new_user


@app.get("/users/", response_model=list[User])
def get_users(session: Session = Depends(get_session)) -> list[User]:
    """Get all users."""
    users = session.exec(select(User)).all()
    return users


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("energy_prime_back.main:app", host="0.0.0.0", port=8000, reload=True, workers=1)
