# Description: main.py

## Overview
Entry point of the FastAPI application. Orchestrates configuration loading, database lifecycle events, middleware registration, API routing, and static file mounting.

## Exports & Functions
- `lifespan(app: FastAPI)`
  - **Description**: Async context manager that connects to MongoDB on startup and closes the connection pool on shutdown.
  - **Parameters**: `app` (FastAPI instance)
  - **Returns**: Async generator managing startup and shutdown phases.
- `app: FastAPI`
  - **Description**: The configured FastAPI web application instance.

## Dependencies & Data Flow
- **Imports**: `FastAPI`, `StaticFiles`, `CORSMiddleware`, `config`, `database`, `notice_router`.
- **Invoked By**: Uvicorn server (`uvicorn main:app`).
- **Data Flow**: Reads configuration -> Initializes database lifecycle -> Attaches security headers and CORS -> Mounts API routes under `/api` -> Serves frontend static files from `/static`.
