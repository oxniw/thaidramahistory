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
    sort_by: Optional[str] = "default",
) -> List[Dict[str, Any]]:
    """Query notices with optional filters and custom sorting order."""
    sort_mode = (sort_by or "default").lower()

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

        # In-memory sorting fallback
        if sort_mode == "newest":
            results.sort(key=lambda x: x.get("created_at"), reverse=True)
        elif sort_mode == "oldest":
            results.sort(key=lambda x: x.get("created_at"), reverse=False)
        elif sort_mode == "title_asc":
            results.sort(key=lambda x: x.get("title", "").lower(), reverse=False)
        elif sort_mode == "title_desc":
            results.sort(key=lambda x: x.get("title", "").lower(), reverse=True)
        elif sort_mode == "priority":
            results.sort(key=lambda x: (x.get("priority") != "urgent", not x.get("is_pinned", False), x.get("created_at")), reverse=False)
        else:  # default: pinned first, newest first
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

    # Map sort mode to MongoDB sort specification
    sort_specs = {
        "newest": [("created_at", -1)],
        "oldest": [("created_at", 1)],
        "title_asc": [("title", 1)],
        "title_desc": [("title", -1)],
        "priority": [("priority", -1), ("is_pinned", -1), ("created_at", -1)],
    }
    mongo_sort = sort_specs.get(sort_mode, [("is_pinned", -1), ("created_at", -1)])

    cursor = collection.find(query).sort(mongo_sort)
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
