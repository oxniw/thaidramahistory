# Description: program/main.py

## Overview
Entry point for the local database control portal. Boots a FastAPI server locked strictly to `127.0.0.1:8500`, connects to MongoDB, mounts API routes, and serves the management dashboard.

## Exports & Functions
- `lifespan(app: FastAPI)`
  - **Description**: Async lifecycle manager verifying MongoDB connection on startup and releasing client resources on shutdown.
  - **Parameters**: `app` (FastAPI instance).
  - **Returns**: Async generator.
- `app: FastAPI`
  - **Description**: Configured FastAPI web application instance for local database management.
- `main()`
  - **Description**: CLI startup function that launches Uvicorn bound to `127.0.0.1:8500` and outputs access link.

## Dependencies & Data Flow
- **Imports**: `fastapi.FastAPI`, `fastapi.staticfiles.StaticFiles`, `uvicorn`, `program.config`, `program.routes`, `database`.
- **Invoked By**: Terminal command (`python program/main.py`) or `start_manager.bat`.
- **Data Flow**: CLI startup -> Connects to database -> Mounts routes under `/api` -> Serves local management UI at `http://127.0.0.1:8500`.
