# Description: program/repository.py

## Overview
Direct database layer executing CRUD, bulk export, and bulk import operations against the MongoDB collection for the local control program.

## Exports & Functions
- `list_records() -> list[dict]`
  - **Description**: Fetches all documents from MongoDB sorted by pinned status and timestamp.
  - **Parameters**: None.
  - **Returns**: List of documents with stringified IDs.
- `create_record(data: dict) -> dict`
  - **Description**: Inserts a new document into MongoDB with UTC timestamps.
  - **Parameters**: `data` (dictionary of notice fields).
  - **Returns**: Created document with assigned ID.
- `update_record(record_id: str, fields: dict) -> dict | None`
  - **Description**: Modifies fields of an existing document and updates `updated_at`.
  - **Parameters**: `record_id`, `fields`.
  - **Returns**: Updated document or `None`.
- `delete_record(record_id: str) -> bool`
  - **Description**: Removes document by ID from MongoDB.
  - **Parameters**: `record_id`.
  - **Returns**: True if deleted, False otherwise.
- `export_all_records() -> list[dict]`
  - **Description**: Dumps all collection records (without internal MongoDB IDs) suitable for JSON backup.
  - **Parameters**: None.
  - **Returns**: List of clean record dictionaries.
- `import_records(records: list[dict]) -> int`
  - **Description**: Inserts a batch of notice records into MongoDB.
  - **Parameters**: `records` (List of notice dictionaries).
  - **Returns**: Number of inserted documents.

## Dependencies & Data Flow
- **Imports**: `bson.ObjectId`, `datetime.datetime`, `program.config.settings`, `motor.motor_asyncio.AsyncIOMotorClient`.
- **Invoked By**: `program/service.py`.
- **Data Flow**: Program requests -> Motor collection queries -> MongoDB.
