# Description: frontend.md

## Overview
Documents the client-side user interface components (`static/index.html`, `static/styles.css`, and `static/app.js`). Implements the high-contrast monochrome brutalist Thaidramahistory archive board displaying notices from MongoDB with keyword search, category filtering, and safe DOM rendering.

## Exports & Functions (app.js)
- `state`: Local state container tracking notices, active filter, search query, and current sort mode (`default`, `newest`, `oldest`, `title_asc`, `title_desc`, `priority`).
- `fetchNotices()`: Calls `GET /api/notices` and triggers board rendering.
- `renderBoard()`: Builds DOM nodes safely using `document.createElement` and `textContent` (preventing XSS) and updates notice counters.
- `createNoticeCardElement(notice)`: Returns a structured notice card element with badges, title, body, author, and date.
- `updateCounters()`: Updates total, pinned, and urgent notice counts.

## Dependencies & Data Flow
- **Assets**: `static/index.html`, `static/styles.css`, `static/app.js`.
- **Invoked By**: User browser loading the root URL `/`.
- **Data Flow**: User interaction -> Fetch API calls to `/api/notices` -> Safe DOM reconciliation without innerHTML injection.
