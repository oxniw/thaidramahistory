# ==============================================================================
# File: .//Description-of-file/program_service.md
# Overview: Business logic and data transformation for local database control.
# ==============================================================================

import json
from typing import List, Dict, Any
from fastapi import HTTPException, status
from program import repository


async def get_all_notices() -> List[Dict[str, Any]]:
    """Return all notices sorted with pinned items first."""
    return await repository.list_records()


async def add_notice(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and persist new notice."""
    title = str(payload.get("title", "")).strip()
    content = str(payload.get("content", "")).strip()

    if not title:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty.")
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty.")

    clean_data = {
        "title": title,
        "content": content,
        "category": str(payload.get("category", "General")).strip() or "General",
        "priority": "urgent" if str(payload.get("priority", "")).lower() == "urgent" else "normal",
        "is_pinned": bool(payload.get("is_pinned", False)),
        "author": str(payload.get("author", "Staff")).strip() or "Staff",
    }
    return await repository.create_record(clean_data)


async def edit_notice(notice_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Modify fields on an existing notice."""
    existing = await repository.get_record_by_id(notice_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notice with id '{notice_id}' was not found.",
        )

    fields_to_update: Dict[str, Any] = {}
    if "title" in payload:
        title = str(payload["title"]).strip()
        if not title:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty.")
        fields_to_update["title"] = title

    if "content" in payload:
        content = str(payload["content"]).strip()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty.")
        fields_to_update["content"] = content

    if "category" in payload:
        fields_to_update["category"] = str(payload["category"]).strip() or "General"

    if "priority" in payload:
        fields_to_update["priority"] = "urgent" if str(payload["priority"]).lower() == "urgent" else "normal"

    if "is_pinned" in payload:
        fields_to_update["is_pinned"] = bool(payload["is_pinned"])

    if "author" in payload:
        fields_to_update["author"] = str(payload["author"]).strip() or "Staff"

    updated = await repository.update_record(notice_id, fields_to_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update record.")
    return updated


async def remove_notice(notice_id: str) -> Dict[str, Any]:
    """Remove notice by ID."""
    success = await repository.delete_record(notice_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notice with id '{notice_id}' does not exist.",
        )
    return {"status": "success", "message": f"Notice '{notice_id}' deleted."}


async def generate_export_payload() -> List[Dict[str, Any]]:
    """Export clean JSON list of notices."""
    return await repository.export_all_records()


async def process_import_bytes(file_bytes: bytes) -> Dict[str, Any]:
    """Parse JSON bytes and import records into database."""
    try:
        data = json.loads(file_bytes.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid JSON format: {exc}")

    if not isinstance(data, list):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="JSON must contain a list of notices.")

    inserted_count = await repository.import_records(data)
    return {
        "status": "success",
        "imported_count": inserted_count,
        "message": f"Successfully imported {inserted_count} notice(s).",
    }
