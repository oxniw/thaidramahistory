# ==============================================================================
# File: .//Description-of-file/models.md
# Overview: Declares Pydantic data schemas for bulletin notices with strict validation.
# ==============================================================================

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class NoticePriority(str, Enum):
    """Allowed priority levels for notices."""
    NORMAL = "normal"
    URGENT = "urgent"


class NoticeBase(BaseModel):
    """Core notice fields shared across models."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Headline or title of the notice",
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Detailed body text of the notice",
    )
    category: str = Field(
        default="General",
        min_length=1,
        max_length=50,
        description="Category tag for filtering",
    )
    priority: NoticePriority = Field(
        default=NoticePriority.NORMAL,
        description="Priority status of the notice",
    )
    is_pinned: bool = Field(
        default=False,
        description="Whether this notice is pinned to top of board",
    )
    author: str = Field(
        default="Administration",
        min_length=1,
        max_length=60,
        description="Display name or department of the poster",
    )

    @field_validator("title", "content", "category", "author", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        """Strip surrounding whitespace from string fields."""
        if isinstance(value, str):
            clean = value.strip()
            if not clean:
                raise ValueError("Field cannot be empty or purely whitespace.")
            return clean
        return value


class NoticeResponse(NoticeBase):
    """Schema returned to API callers with database ID and timestamps."""

    id: str = Field(..., description="Unique 24-character hex identifier")
    created_at: datetime = Field(..., description="Timestamp when notice was created")
    updated_at: datetime = Field(..., description="Timestamp of latest modification")
