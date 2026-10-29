# Description: notice_repository.md

## Overview
Encapsulates all database read operations behind a repository boundary, supporting live MongoDB queries and in-memory seed storage fallback for local development.

## Exports & Functions
- `list_notices(category: str | None = None, priority: str | None = None, search: str | None = None) -> list[dict]`
  - **Description**: Fetches notices matching optional category, priority, or search term, sorted with pinned items first.
  - **Parameters**: `category`, `priority`, `search`.
  - **Returns**: List of notice documents with stringified identifiers.
- `get_notice_by_id(notice_id: str) -> dict | None`
  - **Description**: Retrieves a single notice by its identifier.
  - **Parameters**: `notice_id`.
  - **Returns**: Matching document or `None`.

## Dependencies & Data Flow
- **Imports**: `bson.ObjectId`, `datetime.datetime`, `database.get_collection`, `database.is_mongo_connected`.
- **Invoked By**: `notice_service.py`.
- **Data Flow**: Service query parameters -> MongoDB / fallback store -> Serialized dictionaries.
