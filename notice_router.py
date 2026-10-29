# ==============================================================================
# File: .//Description-of-file/notice_router.md
# Overview: HTTP route definitions for the Thaidramahistory REST API.
# ==============================================================================

from typing import Optional, List
from fastapi import APIRouter, Query
from models import NoticeResponse
import notice_service

router = APIRouter(tags=["Notices"])


@router.get("/notices", response_model=List[NoticeResponse], summary="List all notices")
async def get_notices_endpoint(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority (normal, urgent)"),
    search: Optional[str] = Query(None, description="Search term for title or content"),
    sort_by: Optional[str] = Query(
        "default",
        description="Sort order: default (pinned first), newest, oldest, title_asc, title_desc, priority",
    ),
) -> List[NoticeResponse]:
    """Retrieve all notices from the database matching optional query filters and order."""
    return await notice_service.fetch_notices(
        category=category,
        priority=priority,
        search=search,
        sort_by=sort_by,
    )


@router.get("/notices/{notice_id}", response_model=NoticeResponse, summary="Get notice details")
async def get_single_notice_endpoint(notice_id: str) -> NoticeResponse:
    """Retrieve details for a single notice by identifier."""
    return await notice_service.fetch_notice(notice_id)
