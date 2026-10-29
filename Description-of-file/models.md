# Description: models.py

## Overview
Declares Pydantic data schemas for bulletin board notices, including creation, update, and API response representations with strict validation constraints.

## Exports & Functions
- `NoticePriority(str, Enum)`: Allowed priority values (`normal`, `urgent`).
- `NoticeBase(BaseModel)`: Core attributes shared across input and output schemas.
  - `title: str` (length 1-150)
  - `content: str` (length 1-5000)
  - `category: str` (length 1-50)
  - `priority: NoticePriority`
  - `is_pinned: bool`
  - `author: str` (length 1-60)
- `NoticeCreate(NoticeBase)`: Schema used for incoming notice creation requests.
- `NoticeUpdate(BaseModel)`: Schema for partial notice updates with optional fields.
- `NoticeResponse(NoticeBase)`: Schema serialized back to API callers including database generated identifier and timestamps.
  - `id: str`
  - `created_at: datetime`
  - `updated_at: datetime`

## Dependencies & Data Flow
- **Imports**: `pydantic.BaseModel`, `pydantic.Field`, `enum.Enum`, `datetime.datetime`.
- **Invoked By**: `notice_repository.py`, `notice_service.py`, `notice_router.py`.
- **Data Flow**: HTTP request payload -> Pydantic validation -> Service processing -> Serialized HTTP response.
