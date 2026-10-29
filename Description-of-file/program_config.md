# Description: program/config.py

## Overview
Declares runtime configuration for the local database control portal, reading `.env` for database connection details while enforcing localhost-only binding.

## Exports & Functions
- `ProgramSettings(BaseSettings)`
  - `HOST: str = "127.0.0.1"` (Strict localhost lockdown)
  - `PORT: int = 8500` (Dedicated local management port)
  - `MONGODB_URI: str` (Loaded from root `.env`)
  - `DATABASE_NAME: str`
  - `COLLECTION_NAME: str`
- `settings: ProgramSettings`
  - **Description**: Singleton configuration instance.

## Dependencies & Data Flow
- **Imports**: `pydantic_settings.BaseSettings`, `pydantic.Field`, `pathlib.Path`.
- **Invoked By**: `program/main.py`, `program/repository.py`.
- **Data Flow**: `.env` file -> Pydantic settings -> Program modules.
