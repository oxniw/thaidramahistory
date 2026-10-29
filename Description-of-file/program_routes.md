# Description: program/routes.py

## Overview
Declares FastAPI route handlers for the local control portal, providing endpoints for notice management, JSON backups, and batch imports.

## Exports & Functions
- `router: APIRouter`: Router mounted under `/api`.
- `list_notices_endpoint() -> list[dict]` (`GET /api/notices`)
- `create_notice_endpoint(payload: dict) -> dict` (`POST /api/notices`)
- `update_notice_endpoint(notice_id: str, payload: dict) -> dict` (`PUT /api/notices/{notice_id}`)
- `delete_notice_endpoint(notice_id: str) -> dict` (`DELETE /api/notices/{notice_id}`)
- `export_notices_endpoint()` (`GET /api/export` - triggers JSON file download)
- `import_notices_endpoint(file: UploadFile)` (`POST /api/import` - accepts JSON file upload)

## Dependencies & Data Flow
- **Imports**: `fastapi.APIRouter`, `fastapi.UploadFile`, `fastapi.responses.JSONResponse`, `program.service`.
- **Invoked By**: `program/main.py`.
- **Data Flow**: Local browser requests -> Route handlers -> Service actions -> JSON responses.
