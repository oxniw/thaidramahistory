# Description: config.py

## Overview
Centralizes application configuration, environment variable parsing, and default settings using Pydantic Settings.

## Exports & Functions
- `Settings`: Pydantic model loading environment variables with defaults.
  - `APP_NAME: str`
  - `PORT: int`
  - `HOST: str`
  - `MONGODB_URI: str`
  - `DATABASE_NAME: str`
  - `COLLECTION_NAME: str`
  - `CORS_ORIGINS: list[str]`
- `settings: Settings`
  - **Description**: Singleton configuration object initialized from environment variables or `.env`.

## Dependencies & Data Flow
- **Imports**: `pydantic_settings.BaseSettings`, `pydantic.Field`.
- **Invoked By**: `database.py`, `main.py`.
- **Data Flow**: System environment variables & `.env` file -> Pydantic validation -> Exported `settings` object.
