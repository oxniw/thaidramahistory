# Monochrome Notice Board

A minimalist, high-contrast monochrome notice and bulletin board web application built with Python FastAPI and MongoDB, styled with a brutalist black-and-white theme and ready for deployment on [Render.com](https://render.com).

---

## Features

- **High-Contrast Monochrome Design**: Sharp black-and-white typography, brutalist borders, pinned callouts, and responsive grid layout.
- **FastAPI Backend**: Asynchronous architecture powered by `FastAPI`, `Motor`, and `Pydantic`.
- **MongoDB Storage**: Scalable document storage for notices, categories, tags, and timestamps.
- **Admin Access Control**: Mutating routes (`POST`, `PUT`, `DELETE`) require an administrative passkey verified using constant-time string comparison (`secrets.compare_digest`).
- **Security-First**: Input length validation, safe DOM rendering (preventing XSS), defense-in-depth HTTP security headers, and safe exception masking.
- **Separated Function Architecture**: Strict separation of concerns across config, database, models, repository, service, router, and documentation.
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
│   ├── auth_service.md
│   ├── notice_router.md
│   └── frontend.md
├── static/                     # Frontend client assets
│   ├── index.html              # Single page layout
│   ├── styles.css              # Monochrome brutalist CSS
│   └── app.js                  # Safe DOM controller & admin logic
├── config.py                   # Pydantic Settings & environment variables
├── database.py                 # Async Motor MongoDB connection pool
├── models.py                   # Pydantic data schemas with strict validation
├── notice_repository.py        # MongoDB persistence seam
├── notice_service.py           # Domain business rules and sanitization
├── auth_service.py             # Administrative key verification
├── notice_router.py            # API route handlers
├── main.py                     # Entry point orchestrating FastAPI app
├── render.yaml                 # Render.com Blueprint configuration
├── Procfile                    # Process file for Render web service
├── requirements.txt            # Python dependencies
├── .env.example                # Sample environment variables
└── README.md                   # Project documentation
```

---

## Local Development

### 1. Prerequisites
- Python 3.10+
- MongoDB instance (local MongoDB server or free [MongoDB Atlas](https://www.mongodb.com/atlas) cluster)

### 2. Setup Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```
Edit `.env` and provide your MongoDB URI and custom admin passkey:
```ini
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=bulletin_board
COLLECTION_NAME=notices
ADMIN_API_KEY=your-secure-admin-passkey-here
PORT=8000
APP_ENV=development
```

### 5. Start Server
```bash
uvicorn main:app --reload --port 8000
```
Open your browser at `http://localhost:8000`.

---

## Deploying to Render.com

### Option A: Using Render Blueprint (`render.yaml`)
1. Push this repository to GitHub or GitLab.
2. In the [Render Dashboard](https://dashboard.render.com), click **New +** and select **Blueprint**.
3. Connect your repository. Render will detect `render.yaml`.
4. In the environment configuration, supply your `MONGODB_URI` (from MongoDB Atlas).
5. Render will automatically install dependencies, configure the health probe at `/health`, and launch the web service.

### Option B: Manual Web Service Setup
1. In the Render Dashboard, click **New +** -> **Web Service**.
2. Connect your repository.
3. Configure settings:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add the following Environment Variables under the **Environment** tab:
   - `MONGODB_URI`: your MongoDB Atlas connection string.
   - `ADMIN_API_KEY`: your secret administrative passkey.
   - `DATABASE_NAME`: `bulletin_board`
   - `COLLECTION_NAME`: `notices`
   - `PYTHON_VERSION`: `3.12.10`
5. Click **Create Web Service**.

---

## API Reference

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/health` | Service health check | No |
| `GET` | `/api/notices` | Fetch notices (supports `category`, `priority`, `search`) | No |
| `GET` | `/api/notices/{id}` | Get single notice details | No |
| `POST` | `/api/notices` | Create a new notice | Yes (`X-Admin-Key`) |
| `PUT` | `/api/notices/{id}` | Update existing notice | Yes (`X-Admin-Key`) |
| `DELETE` | `/api/notices/{id}` | Delete notice | Yes (`X-Admin-Key`) |
| `GET` | `/api/auth/verify` | Check admin key validity | Yes (`X-Admin-Key`) |

Interactive Swagger documentation is available at `/docs` when running the application.

---

## Administrative Actions

1. Click the **ADMIN ACCESS** button in the header.
2. Enter the passkey set in `ADMIN_API_KEY`.
3. Once authenticated:
   - The **+ NEW NOTICE** button appears in the header.
   - Each notice card displays **PIN / UNPIN**, **EDIT**, and **DELETE** controls.
