"""Application configuration."""
from typing import Optional
from functools import reduce

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_SERVER: Optional[str]
    POSTGRES_PORT: Optional[str]
    POSTGRES_DB: Optional[str]
    DATABASE_URL: Optional[str]

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

    class Config:
        """Configuration class."""

        env_file = ".env"


settings = Settings()
