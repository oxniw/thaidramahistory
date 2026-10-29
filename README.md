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
│   └── test_suite.md
├── static/                     # Frontend client assets
│   ├── index.html              # Monochrome brutalist layout
│   ├── styles.css              # Black-and-white brutalist CSS
│   └── app.js                  # Safe DOM controller & search/filter logic
├── config.py                   # Pydantic Settings & environment variables
├── database.py                 # Async Motor MongoDB connection pool
├── models.py                   # Pydantic data schemas
├── notice_repository.py        # MongoDB persistence seam with offline fallback
├── notice_service.py           # Domain business rules and sorting
├── notice_router.py            # Public read API routes
├── main.py                     # Entry point orchestrating FastAPI app
├── seed.py                     # Standalone CLI seeder script
├── seed_data.json              # Initial notice dataset
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

### 4. Start the Application
```powershell
uvicorn main:app --reload --port 8000
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser.

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
