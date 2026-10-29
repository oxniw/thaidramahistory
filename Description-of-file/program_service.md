# Description: program/service.md

## Overview
Business logic layer for the database control portal. Handles data validation, string trimming, JSON backup generation, and batch file parsing.

## Exports & Functions
- `get_all_notices() -> list[dict]`
  - **Description**: Returns all notices formatted for the management interface.
  - **Parameters**: None.
  - **Returns**: List of notices.
- `add_notice(payload: dict) -> dict`
  - **Description**: Validates required fields, formats priority, and inserts record.
  - **Parameters**: `payload` (Notice fields).
  - **Returns**: Created notice dict.
- `edit_notice(notice_id: str, payload: dict) -> dict`
  - **Description**: Validates ID, updates record, and returns the modified result.
  - **Parameters**: `notice_id`, `payload`.
  - **Returns**: Modified notice dict.
- `remove_notice(notice_id: str) -> dict`
  - **Description**: Deletes notice by ID or raises 404.
  - **Parameters**: `notice_id`.
  - **Returns**: Status confirmation dictionary.
- `generate_export_payload() -> list[dict]`
  - **Description**: Formats database dump into clean JSON export format.
  - **Parameters**: None.
  - **Returns**: List of notice dictionaries ready for download.
- `process_import_payload(records: list[dict]) -> dict`
  - **Description**: Validates schema of imported items and inserts them into database.
  - **Parameters**: `records`.
  - **Returns**: Import summary dictionary.

## Dependencies & Data Flow
- **Imports**: `fastapi.HTTPException`, `program.repository`.
- **Invoked By**: `program/routes.py`.
- **Data Flow**: HTTP payload -> Validation & transformation -> Repository queries -> Service output.
