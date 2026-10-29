# ==============================================================================
# File: .//Description-of-file/database.md
# Overview: Manages Motor MongoDB connection lifecycle and collection access.
# ==============================================================================

import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from config import settings

logger = logging.getLogger("app.database")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None
_is_connected: bool = False


async def connect_to_mongo() -> None:
    """Initialize MongoDB connection pool and verify connection status."""
    global _client, _db, _is_connected
    try:
        logger.info("Initializing MongoDB connection to configured database...")
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
        )
        _db = _client[settings.DATABASE_NAME]

        # Verify connectivity via admin ping command
        await _client.admin.command("ping")
        _is_connected = True
        logger.info("Successfully established connection to MongoDB.")
    except Exception as exc:
        _is_connected = False
        logger.warning(
            "MongoDB is not currently reachable (%s). Falling back to local example storage for offline/demo use.",
            str(exc),
        )


async def close_mongo_connection() -> None:
    """Close MongoDB connection pool gracefully during shutdown."""
    global _client, _db, _is_connected
    if _client is not None:
        logger.info("Closing MongoDB connection pool...")
        _client.close()
        _client = None
        _db = None
        _is_connected = False
        logger.info("MongoDB connection pool closed.")


def is_mongo_connected() -> bool:
    """Check whether a verified connection to MongoDB is currently active."""
    return _is_connected


def get_database() -> AsyncIOMotorDatabase:
    """Return the active MongoDB database handle."""
    if _db is None:
        raise RuntimeError("Database connection has not been initialized.")
    return _db


def get_collection(name: Optional[str] = None) -> AsyncIOMotorCollection:
    """Return collection handle from active database."""
    collection_name = name or settings.COLLECTION_NAME
    return get_database()[collection_name]
