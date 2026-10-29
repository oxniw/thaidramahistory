# ==============================================================================
# File: .//Description-of-file/notice_service.md
# Overview: Orchestrates domain business logic and retrieval rules for notices.
# ==============================================================================

from typing import Optional, List
from fastapi import HTTPException, status
from models import NoticeResponse
import notice_repository


async def fetch_notices(
    category: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: Optional[str] = "default",
) -> List[NoticeResponse]:
    """Retrieve filtered and sorted notices from storage."""
    docs = await notice_repository.list_notices(
        category=category,
        priority=priority,
        search=search,
        sort_by=sort_by,
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
