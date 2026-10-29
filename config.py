# ==============================================================================
# File: .//Description-of-file/config.md
# Overview: Centralizes application configuration and environment variables.
# ==============================================================================

import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Monochrome Notice Board"
    APP_ENV: str = "production"
    PORT: int = Field(default=8000, alias="PORT")
    HOST: str = "0.0.0.0"

    # MongoDB connection details
    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection string (e.g. MongoDB Atlas or local URI)",
    )
    DATABASE_NAME: str = "bulletin_board"
    COLLECTION_NAME: str = "notices"

    # Admin key for creating, editing, and deleting notices
    ADMIN_API_KEY: str = Field(
        default="admin-change-this-secret",
        description="Administrative secret key for mutating notice endpoints",
    )

    # CORS origins
    CORS_ORIGINS: list[str] = ["*"]


settings = Settings()
