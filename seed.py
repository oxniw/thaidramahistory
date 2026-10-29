# ==============================================================================
# File: .//Description-of-file/seed.md
# Overview: Standalone script populating MongoDB with example notice records.
# ==============================================================================

import asyncio
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed")

SEED_FILE = Path(__file__).resolve().parent / "seed_data.json"


def load_seed_records(filepath: Path) -> List[Dict[str, Any]]:
    """Read and parse initial notice definitions from a JSON file."""
    if not filepath.exists():
        raise FileNotFoundError(f"Seed file not found at: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


async def seed_database() -> int:
    """Connect to MongoDB and insert example notices if database is empty."""
    logger.info("Connecting to MongoDB at: %s", settings.MONGODB_URI)
    client = AsyncIOMotorClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=5000,
    )
    db = client[settings.DATABASE_NAME]
    collection = db[settings.COLLECTION_NAME]

    # Verify connection
    await client.admin.command("ping")
    logger.info("Successfully connected to MongoDB.")

    # Check existing documents
    existing_count = await collection.count_documents({})
    if existing_count > 0:
        logger.info(
            "Collection '%s' already contains %d document(s). Skipping seed to preserve data.",
            settings.COLLECTION_NAME,
            existing_count,
        )
        client.close()
        return 0

    records = load_seed_records(SEED_FILE)
    now = datetime.now(timezone.utc)

    prepared_docs = []
    for item in records:
        doc = dict(item)
        doc["created_at"] = now
        doc["updated_at"] = now
        prepared_docs.append(doc)

    result = await collection.insert_many(prepared_docs)
    inserted_count = len(result.inserted_ids)
    logger.info("Inserted %d example notices into '%s'.", inserted_count, settings.COLLECTION_NAME)

    client.close()
    return inserted_count


def main():
    """Entry point for standalone CLI execution."""
    try:
        count = asyncio.run(seed_database())
        print(f"Seed completed: {count} notice(s) created.")
    except Exception as exc:
        logger.error("Failed to seed MongoDB: %s", exc)
        print("Could not complete seeding. Verify your MONGODB_URI connection.")


if __name__ == "__main__":
    main()
