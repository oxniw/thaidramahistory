# Description: notice_service.md

## Overview
Coordinates business domain retrieval rules and formats notices for public presentation.

## Exports & Functions
- `fetch_notices(category: str | None = None, priority: str | None = None, search: str | None = None, sort_by: str | None = "default") -> list[NoticeResponse]`
  - **Description**: Retrieves and sorts notices from the repository according to chosen sort order (`default`, `newest`, `oldest`, `title_asc`, `title_desc`, `priority`).
  - **Parameters**: Optional filter and sorting criteria.
  - **Returns**: List of validated `NoticeResponse` objects.
- `fetch_notice(notice_id: str) -> NoticeResponse`
  - **Description**: Retrieves a single notice by ID or raises HTTP 404 if not found.
  - **Parameters**: `notice_id`.
  - **Returns**: Validated `NoticeResponse`.

## Dependencies & Data Flow
- **Imports**: `models`, `notice_repository`, `fastapi.HTTPException`.
- **Invoked By**: `notice_router.py`.
- **Data Flow**: Controller models -> Repository queries -> Domain models returned to caller.
