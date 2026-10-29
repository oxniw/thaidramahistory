# Description: notice_router.md

## Overview
Declares public read-only HTTP route definitions for the Notice Board REST API.

## Exports & Functions
- `router: APIRouter`: Configured FastAPI router under prefix `/api`.
- `get_notices_endpoint(...) -> list[NoticeResponse]`
  - **Route**: `GET /api/notices`
  - **Description**: Returns all public notices matching optional query parameters (`category`, `priority`, `search`).
- `get_single_notice_endpoint(notice_id: str) -> NoticeResponse`
  - **Route**: `GET /api/notices/{notice_id}`
  - **Description**: Returns details for a single notice by ID.

## Dependencies & Data Flow
- **Imports**: `fastapi.APIRouter`, `fastapi.Query`, `models.NoticeResponse`, `notice_service`.
- **Invoked By**: `main.py`.
- **Data Flow**: HTTP Client requests -> Endpoint handlers -> Service functions -> JSON responses.
