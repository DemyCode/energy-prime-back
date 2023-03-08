"""Application configuration."""
from functools import reduce
from typing import Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str
    PROJECT_VERSION: str

    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_SERVER: Optional[str]
    POSTGRES_PORT: Optional[str]
    POSTGRES_DB: Optional[str]
    DATABASE_URL: Optional[str] = "sqlite:///database.sqlite"

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> Optional[str]:
        """Assemble database connection URL."""
        if isinstance(v, str):
            return v
        if reduce(
            lambda x, y: x and y,
            [
                values.get(x) is None
                for x in [
                    "POSTGRES_USER",
                    "POSTGRES_PASSWORD",
                    "POSTGRES_SERVER",
                    "POSTGRES_PORT",
                    "POSTGRES_DB",
                ]
            ],
        ):
            raise ValueError("Database not properly configured. Please check your .env file.")
        return (
            f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@"
            + f"{values.get('POSTGRES_SERVER')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}"
        )

    ALCHEMY_UPGRADE: Optional[bool] = False

    @validator("ALCHEMY_UPGRADE", pre=True)
    def warn_alchemy_upgrade(cls, v: Optional[bool], values: dict) -> Optional[bool]:
        """Warn about alembic upgrade."""
        if v is not None and v is True and values.get("CREATE_TABLES") is True:
            raise ValueError("Cannot set ALCHEMY_UPGRADE and CREATE_TABLES to True at the same time.")
        return v

    CREATE_TABLES: Optional[bool] = True

    class Config:
        """Configuration class."""

        env_file = ".env"


settings = Settings(PROJECT_NAME="FastAPI", PROJECT_VERSION="0.1.0")  # type: ignore
