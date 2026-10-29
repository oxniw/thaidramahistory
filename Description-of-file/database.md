# Description: database.py

## Overview
Manages the asynchronous Motor MongoDB client connection pool and provides access to database collections.

## Exports & Functions
- `connect_to_mongo() -> None`
  - **Description**: Initializes the Motor async MongoDB client using the configured connection URI.
  - **Parameters**: None.
  - **Returns**: None.
- `close_mongo_connection() -> None`
  - **Description**: Gracefully closes the MongoDB client connection pool.
  - **Parameters**: None.
  - **Returns**: None.
- `is_mongo_connected() -> bool`
  - **Description**: Returns True if active MongoDB cluster ping succeeded, False otherwise.
  - **Parameters**: None.
  - **Returns**: `bool`
- `get_database()`
  - **Description**: Returns the active MongoDB database instance.
  - **Parameters**: None.
  - **Returns**: `AsyncIOMotorDatabase`
- `get_collection(name: str | None = None)`
  - **Description**: Returns a MongoDB collection handle.
  - **Parameters**: `name` (optional collection name override).
  - **Returns**: `AsyncIOMotorCollection`

## Dependencies & Data Flow
- **Imports**: `motor.motor_asyncio.AsyncIOMotorClient`, `config.settings`.
- **Invoked By**: `main.py` (lifespan hook), `notice_repository.py`.
- **Data Flow**: `settings.MONGODB_URI` -> Motor client pool -> MongoDB collection queries.
