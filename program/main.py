# ==============================================================================
# File: .//Description-of-file/program_main.md
# Overview: Entry point initializing FastAPI and Uvicorn for local database manager.
# ==============================================================================

import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure root directory is in sys.path when executed directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from program.config import settings
from program.repository import init_connection, close_connection
from program.routes import router as manager_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager verifying database connection on startup."""
    await init_connection()
    yield
    await close_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# Register management API routes
app.include_router(manager_router)

# Mount local manager frontend
STATIC_DIR = Path(__file__).resolve().parent / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_dashboard():
        """Serve the local database management control dashboard."""
        return FileResponse(STATIC_DIR / "index.html")


def run():
    """Start local management server strictly on localhost."""
    import uvicorn
    import webbrowser

    url = f"http://{settings.HOST}:{settings.PORT}"
    print("==================================================")
    print(f"THAIDRAMAHISTORY - DATABASE CONTROL PORTAL")
    print(f"Locked to localhost: {url}")
    print("==================================================")

    try:
        webbrowser.open(url)
    except Exception:
        pass

    uvicorn.run(
        "program.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
    )


if __name__ == "__main__":
    run()
