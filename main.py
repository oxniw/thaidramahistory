# ==============================================================================
# File: .//Description-of-file/main.md
# Overview: Entry point initializing FastAPI, middleware, routes, and static assets.
# ==============================================================================

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config import settings
from database import connect_to_mongo, close_mongo_connection
from notice_router import router as notice_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager handling database connection startup and shutdown."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def apply_security_headers(request: Request, call_next):
    """Enforce defense-in-depth security headers on all HTTP responses."""
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# Health check endpoint for Render.com zero-downtime health probes
@app.get("/health", tags=["Health"])
async def health_check():
    """Health status probe for deployment monitors."""
    return {"status": "ok"}


# Register Notice API routes
app.include_router(notice_api_router, prefix="/api")

# Static assets directory
STATIC_DIR = Path(__file__).resolve().parent / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        """Serve the frontend single page application."""
        return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
    )
