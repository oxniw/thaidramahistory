# ==============================================================================
# File: .//Description-of-file/notice_repository.md
# Overview: Encapsulates MongoDB database read operations behind a repository seam.
# ==============================================================================

import json
import logging
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
from bson import ObjectId
from bson.errors import InvalidId
from database import get_collection, is_mongo_connected

logger = logging.getLogger("app.repository")
SEED_FILE = Path(__file__).resolve().parent / "seed_data.json"

# In-memory storage fallback for local/offline execution
_local_store: List[Dict[str, Any]] = []
_local_initialized: bool = False


def _init_local_store() -> None:
    """Initialize local memory store from seed data if not yet initialized."""
    global _local_store, _local_initialized
    if _local_initialized:
        return
    if SEED_FILE.exists():
        try:
            with open(SEED_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
            now = datetime.now(timezone.utc)
            for item in records:
                doc = dict(item)
                doc["id"] = uuid.uuid4().hex[:24]
                doc["created_at"] = now
                doc["updated_at"] = now
                _local_store.append(doc)
            logger.info("Loaded %d example notices into in-memory storage.", len(_local_store))
        except Exception as e:
            logger.warning("Could not load seed_data.json: %s", e)
    _local_initialized = True


def _serialize_document(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Transform internal MongoDB document into domain dictionary with string id."""
    if not doc:
        return None
    data = dict(doc)
    if "_id" in data:
        data["id"] = str(data.pop("_id"))
    return data


async def list_notices(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Query notices with optional filters and convert _id to id."""
    if not is_mongo_connected():
        _init_local_store()
        results = list(_local_store)
        if category:
            results = [n for n in results if n.get("category", "").lower() == category.lower()]
        if priority:
            results = [n for n in results if n.get("priority", "").lower() == priority.lower()]
        if search:
            s = search.lower()
            results = [
                n for n in results
                if s in n.get("title", "").lower() or s in n.get("content", "").lower() or s in n.get("author", "").lower()
            ]
        results.sort(key=lambda x: (not x.get("is_pinned", False), x.get("created_at")), reverse=False)
        return results

    collection = get_collection()
    query: Dict[str, Any] = {}

    if category:
        query["category"] = category

    if priority:
        query["priority"] = priority

    if search:
        escaped_search = re.escape(search.strip())
        query["$or"] = [
            {"title": {"$regex": escaped_search, "$options": "i"}},
            {"content": {"$regex": escaped_search, "$options": "i"}},
            {"author": {"$regex": escaped_search, "$options": "i"}},
        ]

    # Sort pinned items first, then descending by creation date
    cursor = collection.find(query).sort([("is_pinned", -1), ("created_at", -1)])
    docs = await cursor.to_list(length=500)
    return [_serialize_document(doc) for doc in docs if doc is not None]


async def get_notice_by_id(notice_id: str) -> Optional[Dict[str, Any]]:
    """Fetch single document by its ObjectId or local id."""
    if not is_mongo_connected():
        _init_local_store()
        for doc in _local_store:
            if doc.get("id") == notice_id:
                return dict(doc)
        return None

    try:
        oid = ObjectId(notice_id)
    except (InvalidId, TypeError):
        return None

    collection = get_collection()
    doc = await collection.find_one({"_id": oid})
    return _serialize_document(doc)
