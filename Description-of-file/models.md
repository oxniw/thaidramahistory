# Description: models.py

## Overview
Declares Pydantic data schemas for bulletin board notices with strict validation constraints for public display.

## Exports & Functions
- `NoticePriority(str, Enum)`: Allowed priority values (`normal`, `urgent`).
- `NoticeBase(BaseModel)`: Core attributes shared across schemas.
  - `title: str` (length 1-150)
  - `content: str` (length 1-5000)
  - `category: str` (length 1-50)
  - `priority: NoticePriority`
  - `is_pinned: bool`
  - `author: str` (length 1-60)
- `NoticeResponse(NoticeBase)`: Schema serialized back to API callers including database generated identifier and timestamps.
  - `id: str`
  - `created_at: datetime`
  - `updated_at: datetime`

## Dependencies & Data Flow
- **Imports**: `pydantic.BaseModel`, `pydantic.Field`, `enum.Enum`, `datetime.datetime`.
- **Invoked By**: `notice_repository.py`, `notice_service.py`, `notice_router.py`.
- **Data Flow**: MongoDB documents / local store -> Service mapping -> Pydantic serialization -> HTTP response.
