# Description: notice_repository.md

## Overview
Encapsulates all database interactions behind a repository boundary, supporting live MongoDB collections and fallback in-memory seed storage for offline development and local preview.

## Exports & Functions
- `list_notices(category: str | None = None, priority: str | None = None, search: str | None = None) -> list[dict]`
  - **Description**: Fetches notices from MongoDB matching optional category, priority, or text search filters.
  - **Parameters**: `category`, `priority`, `search`.
  - **Returns**: List of notice documents with stringified identifiers.
- `get_notice_by_id(notice_id: str) -> dict | None`
  - **Description**: Retrieves a single notice by its MongoDB ObjectId.
  - **Parameters**: `notice_id` (24-character hexadecimal ID).
  - **Returns**: Matching document or `None`.
- `insert_notice(data: dict) -> dict`
  - **Description**: Inserts a new notice document into MongoDB with creation and update timestamps.
  - **Parameters**: `data` (dictionary of notice fields).
  - **Returns**: The inserted notice document including generated `_id`.
- `update_notice_by_id(notice_id: str, fields: dict) -> dict | None`
  - **Description**: Updates specified fields of a notice and sets `updated_at`.
  - **Parameters**: `notice_id`, `fields` (dictionary of fields to update).
  - **Returns**: Updated document or `None`.
- `delete_notice_by_id(notice_id: str) -> bool`
  - **Description**: Deletes a notice document by ID.
  - **Parameters**: `notice_id`.
  - **Returns**: `True` if a document was deleted, `False` otherwise.

## Dependencies & Data Flow
- **Imports**: `bson.ObjectId`, `datetime.datetime`, `database.get_collection`, `config.settings`.
- **Invoked By**: `notice_service.py`.
- **Data Flow**: Service request dictionaries -> MongoDB collection execution -> Clean python dictionaries with string IDs.
