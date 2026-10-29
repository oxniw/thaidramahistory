# ==============================================================================
# File: .//Description-of-file/notice_service.md
# Overview: Orchestrates domain business logic, data validation, and sorting rules.
# ==============================================================================

from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from models import NoticeCreate, NoticeUpdate, NoticeResponse
import notice_repository


async def fetch_notices(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
) -> List[NoticeResponse]:
    """Retrieve filtered and sorted notices from storage."""
    docs = await notice_repository.list_notices(
        category=category,
        priority=priority,
        search=search,
    )
    return [NoticeResponse(**doc) for doc in docs]


async def fetch_notice(notice_id: str) -> NoticeResponse:
    """Retrieve single notice by identifier or raise 404."""
    doc = await notice_repository.get_notice_by_id(notice_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notice with id '{notice_id}' was not found.",
        )
    return NoticeResponse(**doc)


async def create_new_notice(payload: NoticeCreate) -> NoticeResponse:
    """Persist new notice after preparing document payload."""
    data = payload.model_dump()
    data["priority"] = payload.priority.value
    created_doc = await notice_repository.insert_notice(data)
    return NoticeResponse(**created_doc)


async def modify_notice(notice_id: str, payload: NoticeUpdate) -> NoticeResponse:
    """Update fields provided in payload for existing notice."""
    update_dict: Dict[str, Any] = payload.model_dump(exclude_unset=True)
    if not update_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided to update.",
        )

    if "priority" in update_dict and update_dict["priority"] is not None:
        update_dict["priority"] = update_dict["priority"].value

    updated_doc = await notice_repository.update_notice_by_id(notice_id, update_dict)
    if not updated_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notice with id '{notice_id}' does not exist.",
        )
    return NoticeResponse(**updated_doc)


async def remove_notice(notice_id: str) -> Dict[str, Any]:
    """Delete notice document by identifier or raise 404."""
    deleted = await notice_repository.delete_notice_by_id(notice_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notice with id '{notice_id}' does not exist or was already removed.",
        )
    return {"status": "success", "message": f"Notice '{notice_id}' removed successfully."}
