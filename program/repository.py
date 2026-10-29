# ==============================================================================
# File: .//Description-of-file/program_repository.md
# Overview: Direct database persistence and backup operations for MongoDB.
# ==============================================================================

import json
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from program.config import settings

logger = logging.getLogger("program.repository")
ROOT_SEED_FILE = Path(__file__).resolve().parent.parent / "seed_data.json"

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None
_is_connected: bool = False

# Fallback store if MongoDB service is not currently active
_local_store: List[Dict[str, Any]] = []
_local_initialized: bool = False


def _init_local_store() -> None:
    """Load initial items into in-memory store if offline."""
    global _local_store, _local_initialized
    if _local_initialized:
        return
    if ROOT_SEED_FILE.exists():
        try:
            with open(ROOT_SEED_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
            now = datetime.now(timezone.utc)
            for item in records:
                doc = dict(item)
                doc["id"] = uuid.uuid4().hex[:24]
                doc["created_at"] = now
                doc["updated_at"] = now
                _local_store.append(doc)
        except Exception as exc:
            logger.warning("Could not load root seed_data.json: %s", exc)
    _local_initialized = True


async def init_connection() -> bool:
    """Connect to MongoDB and ping database."""
    global _client, _db, _is_connected
    try:
        _client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=3000,
            connectTimeoutMS=3000,
        )
        _db = _client[settings.DATABASE_NAME]
        await _client.admin.command("ping")
        _is_connected = True
        logger.info("Manager successfully connected to MongoDB.")
        return True
    except Exception as exc:
        _is_connected = False
        logger.warning("MongoDB unavailable for manager: %s. Using local memory store.", exc)
        return False


async def close_connection() -> None:
    """Close connection pool."""
    global _client, _db, _is_connected
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        _is_connected = False


def _serialize(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Convert MongoDB _id to string id."""
    if not doc:
        return None
    data = dict(doc)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    return data


async def list_records() -> List[Dict[str, Any]]:
    """Retrieve all notices ordered by pinned status and timestamp."""
    if not _is_connected:
        _init_local_store()
        results = list(_local_store)
        results.sort(key=lambda x: (not x.get("is_pinned", False), x.get("created_at")), reverse=False)
        return results

    coll = _db[settings.COLLECTION_NAME]
    cursor = coll.find({}).sort([("is_pinned", -1), ("created_at", -1)])
    docs = await cursor.to_list(length=1000)
    return [_serialize(doc) for doc in docs if doc is not None]


async def get_record_by_id(record_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve document by ID."""
    if not _is_connected:
        _init_local_store()
        for doc in _local_store:
            if doc.get("id") == record_id:
                return dict(doc)
        return None

    try:
        oid = ObjectId(record_id)
    except (InvalidId, TypeError):
        return None

    coll = _db[settings.COLLECTION_NAME]
    doc = await coll.find_one({"_id": oid})
    return _serialize(doc)


async def create_record(data: Dict[str, Any]) -> Dict[str, Any]:
    """Insert a new document into MongoDB with timestamps."""
    now = datetime.now(timezone.utc)
    doc_to_insert = dict(data)
    doc_to_insert["created_at"] = now
    doc_to_insert["updated_at"] = now

    if not _is_connected:
        _init_local_store()
        doc_to_insert["id"] = uuid.uuid4().hex[:24]
        _local_store.insert(0, doc_to_insert)
        return dict(doc_to_insert)

    coll = _db[settings.COLLECTION_NAME]
    result = await coll.insert_one(doc_to_insert)
    doc_to_insert["_id"] = result.inserted_id
    return _serialize(doc_to_insert)  # type: ignore


async def update_record(record_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update fields on existing notice."""
    now = datetime.now(timezone.utc)
    if not _is_connected:
        _init_local_store()
        for idx, doc in enumerate(_local_store):
            if doc.get("id") == record_id:
                updated = dict(doc)
                updated.update(fields)
                updated["updated_at"] = now
                _local_store[idx] = updated
                return dict(updated)
        return None

    try:
        oid = ObjectId(record_id)
    except (InvalidId, TypeError):
        return None

    coll = _db[settings.COLLECTION_NAME]
    update_data = dict(fields)
    update_data["updated_at"] = now

    updated_doc = await coll.find_one_and_update(
        {"_id": oid},
        {"$set": update_data},
        return_document=True,
    )
    return _serialize(updated_doc)


async def delete_record(record_id: str) -> bool:
    """Delete document by ID."""
    if not _is_connected:
        _init_local_store()
        initial_len = len(_local_store)
        _local_store[:] = [n for n in _local_store if n.get("id") != record_id]
        return len(_local_store) < initial_len

    try:
        oid = ObjectId(record_id)
    except (InvalidId, TypeError):
        return False

    coll = _db[settings.COLLECTION_NAME]
    result = await coll.delete_one({"_id": oid})
    return result.deleted_count > 0


async def export_all_records() -> List[Dict[str, Any]]:
    """Export clean notice records without internal database IDs."""
    raw_docs = await list_records()
    export_list = []
    for doc in raw_docs:
        item = {
            "title": doc.get("title", ""),
            "content": doc.get("content", ""),
            "category": doc.get("category", "General"),
            "priority": doc.get("priority", "normal"),
            "is_pinned": bool(doc.get("is_pinned", False)),
            "author": doc.get("author", "Staff"),
        }
        export_list.append(item)
    return export_list


async def import_records(records: List[Dict[str, Any]]) -> int:
    """Insert batch of records into database."""
    now = datetime.now(timezone.utc)
    inserted = 0
    for item in records:
        data = {
            "title": str(item.get("title", "")).strip(),
            "content": str(item.get("content", "")).strip(),
            "category": str(item.get("category", "General")).strip() or "General",
            "priority": "urgent" if str(item.get("priority", "")).lower() == "urgent" else "normal",
            "is_pinned": bool(item.get("is_pinned", False)),
            "author": str(item.get("author", "Staff")).strip() or "Staff",
            "created_at": now,
            "updated_at": now,
        }
        if not data["title"] or not data["content"]:
            continue
        await create_record(data)
        inserted += 1
    return inserted
