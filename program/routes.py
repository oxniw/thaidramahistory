# ==============================================================================
# File: .//Description-of-file/program_routes.md
# Overview: HTTP route definitions for the local database control portal.
# ==============================================================================

import json
from typing import List, Dict, Any
from fastapi import APIRouter, Request, Response, status
from program import service

router = APIRouter(prefix="/api", tags=["Manager"])


@router.get("/notices", response_model=List[Dict[str, Any]])
async def list_notices(sort_by: str = "default"):
    """List all notices currently stored in the database."""
    return await service.get_all_notices(sort_by=sort_by)


@router.post("/notices", status_code=status.HTTP_201_CREATED)
async def create_notice(payload: Dict[str, Any]):
    """Insert a new notice into the database."""
    return await service.add_notice(payload)


@router.put("/notices/{notice_id}")
async def update_notice(notice_id: str, payload: Dict[str, Any]):
    """Update fields of an existing notice."""
    return await service.edit_notice(notice_id, payload)


@router.delete("/notices/{notice_id}")
async def delete_notice(notice_id: str):
    """Delete a notice from the database."""
    return await service.remove_notice(notice_id)


@router.get("/export")
async def export_notices():
    """Download database records as a JSON backup file."""
    records = await service.generate_export_payload()
    json_bytes = json.dumps(records, indent=2, ensure_ascii=False).encode("utf-8")
    return Response(
        content=json_bytes,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=thaidramahistory_backup.json"},
    )


@router.post("/import")
async def import_notices(request: Request):
    """Upload and insert notices from a JSON backup file payload."""
    contents = await request.body()
    return await service.process_import_bytes(contents)
