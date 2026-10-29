# Description: notice_router.md

## Overview
Declares HTTP route definitions for the Notice Board REST API, connecting request endpoints to business services and administrative authorization dependencies.

## Exports & Functions
- `router: APIRouter`: Configured FastAPI router under prefix `/api/notices`.
- `get_notices_endpoint(...) -> list[NoticeResponse]`
  - **Route**: `GET /api/notices`
  - **Description**: Returns all public notices matching optional query parameters.
- `get_single_notice_endpoint(notice_id: str) -> NoticeResponse`
  - **Route**: `GET /api/notices/{notice_id}`
  - **Description**: Returns details for a single notice.
- `create_notice_endpoint(payload: NoticeCreate, admin: str = Depends(verify_admin_key)) -> NoticeResponse`
  - **Route**: `POST /api/notices`
  - **Description**: Creates a new notice. Requires `X-Admin-Key` header.
- `update_notice_endpoint(notice_id: str, payload: NoticeUpdate, admin: str = Depends(verify_admin_key)) -> NoticeResponse`
  - **Route**: `PUT /api/notices/{notice_id}`
  - **Description**: Updates an existing notice. Requires `X-Admin-Key` header.
- `delete_notice_endpoint(notice_id: str, admin: str = Depends(verify_admin_key)) -> dict`
  - **Route**: `DELETE /api/notices/{notice_id}`
  - **Description**: Deletes a notice. Requires `X-Admin-Key` header.
- `verify_admin_status_endpoint(admin: str = Depends(verify_admin_key)) -> dict`
  - **Route**: `GET /api/auth/verify`
  - **Description**: Utility endpoint allowing the frontend to test if an admin key is valid.

## Dependencies & Data Flow
- **Imports**: `fastapi.APIRouter`, `fastapi.Depends`, `fastapi.Query`, `fastapi.status`, `models`, `notice_service`, `auth_service`.
- **Invoked By**: `main.py`.
- **Data Flow**: HTTP Client requests -> Endpoint handlers -> Service functions -> JSON responses.
