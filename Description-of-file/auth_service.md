# Description: auth_service.md

## Overview
Provides admin authorization dependency checks using constant-time string comparison to prevent timing attacks when verifying administrative passkeys.

## Exports & Functions
- `verify_admin_key(x_admin_key: str | None = Header(None)) -> str`
  - **Description**: FastAPI dependency function that validates incoming `X-Admin-Key` header against `config.settings.ADMIN_API_KEY`. Uses `secrets.compare_digest`.
  - **Parameters**: `x_admin_key` (extracted from HTTP request header `X-Admin-Key`).
  - **Returns**: The validated admin key string on success. Raises HTTP 401 Unauthorized if missing or invalid.

## Dependencies & Data Flow
- **Imports**: `secrets`, `fastapi.Header`, `fastapi.HTTPException`, `fastapi.status`, `config.settings`.
- **Invoked By**: `notice_router.py` (applied to POST, PUT, DELETE endpoints).
- **Data Flow**: HTTP header `X-Admin-Key` -> `secrets.compare_digest` -> Route handler execution or 401 response.
