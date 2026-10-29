# ==============================================================================
# File: .//Description-of-file/notice_router.md
# Overview: HTTP route definitions for the Notice Board REST API.
# ==============================================================================

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, Query, status
from models import NoticeCreate, NoticeUpdate, NoticeResponse
from auth_service import verify_admin_key
import notice_service

router = APIRouter(tags=["Notices"])


@router.get("/notices", response_model=List[NoticeResponse], summary="List all notices")
async def get_notices_endpoint(
    category: Optional[str] = Query(None, description="Filter by category"),
    priority: Optional[str] = Query(None, description="Filter by priority (normal, urgent)"),
    search: Optional[str] = Query(None, description="Search term for title or content"),
) -> List[NoticeResponse]:
    """Retrieve all notices matching optional filters."""
    return await notice_service.fetch_notices(
        category=category,
        priority=priority,
        search=search,
    )


@router.get("/notices/{notice_id}", response_model=NoticeResponse, summary="Get notice details")
async def get_single_notice_endpoint(notice_id: str) -> NoticeResponse:
    """Retrieve details for a single notice by identifier."""
    return await notice_service.fetch_notice(notice_id)


@router.post(
    "/notices",
    response_model=NoticeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new notice",
)
async def create_notice_endpoint(
    payload: NoticeCreate,
    _admin: str = Depends(verify_admin_key),
) -> NoticeResponse:
    """Create a new notice card on the bulletin board. Requires admin passkey."""
    return await notice_service.create_new_notice(payload)


@router.put("/notices/{notice_id}", response_model=NoticeResponse, summary="Update notice")
async def update_notice_endpoint(
    notice_id: str,
    payload: NoticeUpdate,
    _admin: str = Depends(verify_admin_key),
) -> NoticeResponse:
    """Modify fields of an existing notice. Requires admin passkey."""
    return await notice_service.modify_notice(notice_id, payload)


@router.delete("/notices/{notice_id}", summary="Delete notice")
async def delete_notice_endpoint(
    notice_id: str,
    _admin: str = Depends(verify_admin_key),
) -> Dict[str, Any]:
    """Remove a notice from the bulletin board. Requires admin passkey."""
    return await notice_service.remove_notice(notice_id)


@router.get("/auth/verify", summary="Verify admin credentials")
async def verify_admin_status_endpoint(
    _admin: str = Depends(verify_admin_key),
) -> Dict[str, str]:
    """Check whether provided admin passkey is valid."""
    return {"status": "authenticated", "message": "Admin authorization verified."}
