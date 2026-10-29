# ==============================================================================
# File: .//Description-of-file/program_config.md
# Overview: Runtime configuration for the local database control portal.
# ==============================================================================

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"


class ProgramSettings(BaseSettings):
    """Configuration for local database management portal."""

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH) if ENV_PATH.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Thaidramahistory Database Manager"
    # Strict localhost lockdown: cannot be accessed across local network
    HOST: str = "127.0.0.1"
    PORT: int = Field(
        default=8500,
        validation_alias="MANAGER_PORT",
        description="Dedicated manager port, separated from public website PORT in .env",
    )

    # MongoDB connection details
    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection string (local or MongoDB Atlas)",
    )
    DATABASE_NAME: str = "bulletin_board"
    COLLECTION_NAME: str = "notices"


settings = ProgramSettings()
