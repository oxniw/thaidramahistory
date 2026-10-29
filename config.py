# ==============================================================================
# File: .//Description-of-file/config.md
# Overview: Centralizes application configuration and environment variables.
# ==============================================================================

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Thaidramahistory"
    PORT: int = Field(default=8000, alias="PORT")
    HOST: str = "0.0.0.0"

    # MongoDB connection details
    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection string (e.g. MongoDB Atlas or local URI)",
    )
    DATABASE_NAME: str = "thaidramahistory"
    COLLECTION_NAME: str = "notices"

    # CORS origins
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
