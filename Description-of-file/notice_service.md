# Description: notice_service.md

## Overview
Coordinates business domain rules, sanitizes text inputs, enforces data constraints, and orders notice items (pinned items first, then descending by creation date).

## Exports & Functions
- `fetch_notices(category: str | None = None, priority: str | None = None, search: str | None = None) -> list[NoticeResponse]`
  - **Description**: Retrieves and sorts notices from the repository according to business sorting rules.
  - **Parameters**: Optional filter criteria.
  - **Returns**: List of validated `NoticeResponse` objects.
- `fetch_notice(notice_id: str) -> NoticeResponse`
  - **Description**: Validates ObjectId format and retrieves a single notice. Raises HTTP 404 if not found or 400 if ID is invalid.
  - **Parameters**: `notice_id`
  - **Returns**: Validated `NoticeResponse`.
- `create_new_notice(payload: NoticeCreate) -> NoticeResponse`
  - **Description**: Sanitizes input strings, constructs creation metadata, and delegates persistence to repository.
  - **Parameters**: `payload` (`NoticeCreate`)
  - **Returns**: The created `NoticeResponse`.
- `modify_notice(notice_id: str, payload: NoticeUpdate) -> NoticeResponse`
  - **Description**: Validates changes, updates the document, and returns the modified result.
  - **Parameters**: `notice_id`, `payload` (`NoticeUpdate`)
  - **Returns**: Updated `NoticeResponse`.
- `remove_notice(notice_id: str) -> dict`
  - **Description**: Validates ID and removes the document from storage.
  - **Parameters**: `notice_id`
  - **Returns**: Status confirmation dictionary.

## Dependencies & Data Flow
- **Imports**: `models`, `notice_repository`, `fastapi.HTTPException`.
- **Invoked By**: `notice_router.py`.
- **Data Flow**: Controller models -> Validation & sanitation -> Repository queries -> Domain models returned to caller.
