# Description: program_frontend.md

## Overview
Documents the client-side user interface of the local database control portal (`program/static/index.html`, `program/static/styles.css`, and `program/static/app.js`). Implements a split management dashboard with an interactive data table on the left, a live create/edit form on the right, and backup/restore controls.

## Exports & Functions (program/static/app.js)
- `loadNotices()`: Fetches database records from `/api/notices` and renders table rows.
- `renderTable(records)`: Populates the left table with status badges, titles, dates, and inline action buttons.
- `populateForm(notice)`: Loads selected notice data into the right editor pane for modification.
- `resetForm()`: Clears editor form and switches back to "Create New" mode.
- `handleSave(event)`: Dispatches `POST` (create) or `PUT` (update) request.
- `handleDelete(id)`: Sends `DELETE` request after user confirmation.
- `handleExport()`: Triggers download of `thaidramahistory_backup.json`.
- `handleImport(file)`: Uploads JSON backup file to `/api/import` and refreshes table.

## Dependencies & Data Flow
- **Assets**: `program/static/index.html`, `program/static/styles.css`, `program/static/app.js`.
- **Invoked By**: Administrator loading `http://127.0.0.1:8500`.
- **Data Flow**: UI user actions -> REST calls to local endpoints -> MongoDB updates -> Table re-render.
