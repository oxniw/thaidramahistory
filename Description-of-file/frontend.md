# Description: frontend.md

## Overview
Documents the client-side user interface components (`static/index.html`, `static/styles.css`, and `static/app.js`). Implements the high-contrast monochrome minimalist brutalist theme with administrative actions, search, category filters, and security-safe DOM rendering.

## Exports & Functions (app.js)
- `state`: Local state container tracking notices, active filter, search query, and stored admin key.
- `fetchNotices()`: Calls `GET /api/notices` and triggers board rendering.
- `renderBoard(notices)`: Builds DOM nodes safely using `document.createElement` and `textContent` (preventing XSS) and updates notice counters.
- `createNoticeCard(notice)`: Returns a structured notice card element with badges, title, body, author, and admin action buttons.
- `handleCreateNotice(formData)`: Sends `POST /api/notices` with `X-Admin-Key` header.
- `handleDeleteNotice(noticeId)`: Confirms and sends `DELETE /api/notices/{id}` with `X-Admin-Key` header.
- `handleTogglePin(notice)`: Sends `PUT /api/notices/{id}` with inverted `is_pinned` status.
- `verifyAdminKey(key)`: Calls `GET /api/auth/verify` to validate administrative credentials.

## Dependencies & Data Flow
- **Assets**: `static/index.html`, `static/styles.css`, `static/app.js`.
- **Invoked By**: User browser loading the root URL `/`.
- **Data Flow**: User interaction -> Fetch API calls to `/api/notices` -> Safe DOM reconciliation without innerHTML injection.
