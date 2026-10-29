# Description: seed.py

## Overview
Standalone database seeding script that populates MongoDB with initial example notice records from `seed_data.json`.

## Exports & Functions
- `load_seed_records(filepath: Path) -> list[dict]`
  - **Description**: Reads and parses initial notice definitions from a JSON file.
  - **Parameters**: `filepath` (Path to JSON seed file).
  - **Returns**: List of notice dictionaries.
- `seed_database() -> int`
  - **Description**: Connects to the configured MongoDB database and inserts example records if the collection is empty.
  - **Parameters**: None.
  - **Returns**: Count of inserted documents.

## Dependencies & Data Flow
- **Imports**: `json`, `datetime`, `asyncio`, `motor.motor_asyncio`, `config.settings`.
- **Invoked By**: Terminal execution (`python seed.py`).
- **Data Flow**: `seed_data.json` -> Parse records -> Motor async client -> MongoDB collection.
