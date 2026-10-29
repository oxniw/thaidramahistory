# Thaidramahistory

A minimalist, high-contrast monochrome bulletin web application built with Python FastAPI and MongoDB, styled with a brutalist black-and-white theme and configured for deployment on [Render.com](https://render.com).

---

## Features

- **High-Contrast Monochrome Design**: Sharp black-and-white typography, brutalist borders, pinned callouts, and responsive grid layout.
- **Pure Read-Only Architecture**: The board reads and renders notices stored in MongoDB without exposing mutation or administrative endpoints.
- **Instant Search & Category Filters**: Client-side filtering across categories (`ALL`, `PINNED`, `URGENT`) and instant keyword search.
- **FastAPI Backend**: Asynchronous architecture powered by `FastAPI`, `Motor`, and `Pydantic`.
- **Security-First**: No write endpoints, safe DOM element construction (preventing XSS), defense-in-depth HTTP security headers, and zero server metadata leakage.
- **Separated Function Architecture**: Strict separation of concerns across configuration, database pool, models, repository, service, router, and documentation.
- **One-Click Render Deployment**: Includes `render.yaml` Blueprint specification and `Procfile`.

---

## Project Structure

```text
thaidramahistory/
├── Description-of-file/        # Documentation folder for every script
│   ├── main.md
│   ├── config.md
│   ├── database.md
│   ├── models.md
│   ├── notice_repository.md
│   ├── notice_service.md
│   ├── notice_router.md
│   ├── frontend.md
│   ├── seed.md
│   ├── test_suite.md
│   ├── program_main.md
│   ├── program_config.md
│   ├── program_repository.md
│   ├── program_service.md
│   ├── program_routes.md
│   ├── program_frontend.md
│   └── program_test.md
├── program/                    # Local-only database management program
│   ├── static/                 # Management split dashboard UI
│   │   ├── index.html
│   │   ├── styles.css
│   │   └── app.js
│   ├── config.py               # Localhost bind settings (127.0.0.1:8500)
│   ├── repository.py           # MongoDB CRUD & backup/restore queries
│   ├── service.py              # Business validation and JSON transformations
│   ├── routes.py               # Manager API routes
│   ├── test_program.py         # Automated test runner for manager
│   └── main.py                 # Manager entry point
├── static/                     # Public frontend client assets
│   ├── index.html              # Monochrome brutalist layout
│   ├── styles.css              # Black-and-white brutalist CSS
│   └── app.js                  # Safe DOM controller & search/filter logic
├── config.py                   # Pydantic Settings & environment variables
├── database.py                 # Async Motor MongoDB connection pool
├── models.py                   # Pydantic data schemas
├── notice_repository.py        # MongoDB persistence seam with offline fallback
├── notice_service.py           # Domain business rules and sorting
├── notice_router.py            # Public read API routes
├── main.py                     # Entry point orchestrating public FastAPI app
├── seed.py                     # Standalone CLI seeder script
├── seed_data.json              # Initial notice dataset
├── start_manager.bat           # Windows one-click launcher for manager
├── test_suite.py               # Automated integration test runner
├── render.yaml                 # Render.com Blueprint configuration
├── Procfile                    # Process file for Render web service
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables
└── README.md                   # Project documentation
```

---

## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```
Provide your MongoDB connection string in `.env` (or use the built-in example dataset out of the box).

### 3. Seed MongoDB (Optional)
To populate an empty MongoDB collection with the example notices:
```powershell
python seed.py
```

### 4. Start the Public Website
```powershell
uvicorn main:app --reload --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## Managing Database Records (Local Control Panel)

To create, edit, delete, pin, import, or export records without exposing admin endpoints on the public website:

### Option A: Windows Batch Launcher
Double-click `start_manager.bat` in the project root.

### Option B: Terminal Command
```powershell
python program/main.py
```

The portal automatically boots at **[http://127.0.0.1:8500](http://127.0.0.1:8500)** strictly bound to localhost:
- **Left Pane**: Searchable records table with instant filter and inline action buttons (`EDIT`, `DEL`).
- **Right Pane**: Live creation and editor form with category, priority, and pin toggles.
- **Top Actions**: One-click **EXPORT JSON** backup download and **IMPORT JSON** restoration.

---

## Running Tests

Run the automated integration test suite:

```powershell
python test_suite.py
```

The test runner validates:
- Health check probe (`GET /health`)
- Static asset serving (`/`, CSS, JS)
- Public notice queries and search filters (`GET /api/notices`)
- Single notice retrieval (`GET /api/notices/{id}`)
- Strict rejection of all mutation methods (`POST`, `PUT`, `DELETE` return `405 Method Not Allowed`)

---

## Deploying to Render.com

1. Push this repository to GitHub or GitLab:
   ```bash
   git add .
   git commit -m "Deploy read-only Thaidramahistory"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```
2. In the [Render Dashboard](https://dashboard.render.com):
   - Click **New +** -> **Blueprint**.
   - Select your repository. Render reads [`render.yaml`](render.yaml).
   - Enter your `MONGODB_URI` under the environment prompt.
   - Click **Apply**. Render builds and deploys your service.
