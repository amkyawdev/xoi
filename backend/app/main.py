import logging
import sys
import os

# Add backend/app to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.routes.auth import router as auth_router
from app.api.routes.chat import router as chat_router
from app.api.routes.history import router as history_router
from app.api.routes.settings import router as settings_router
from app.api.routes.upload import router as upload_router
from app.api.routes.chat_stream import router as chat_stream_router
from app.utils.error_handlers import setup_error_handlers
from app.config import settings
from app.services.auth_service import init_db

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Amkyaw AI Agent API",
    description="Backend API for Amkyaw AI Agent",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allow frontend origins
# In production, only specific origins should be allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://work-1-vlsuqhsmaasxdyuc.prod-runtime.all-hands.dev",
        "https://work-2-vlsuqhsmaasxdyuc.prod-runtime.all-hands.dev",
        "https://xoi-ai.vercel.app",
        "https://xoi-nine.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(chat_stream_router, prefix="/api", tags=["chat-stream"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(history_router, prefix="/api", tags=["history"])
app.include_router(settings_router, prefix="/api", tags=["settings"])
app.include_router(upload_router, prefix="/api", tags=["upload"])


@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Amkyaw AI Agent API starting up...")
    logger.info(f"Version: {settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    # Initialize database
    init_db()
    logger.info("Database initialization completed")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Amkyaw AI Agent API shutting down...")


@app.get("/")
async def root():
    return {
        "message": "Amkyaw AI Agent API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@app.get("/info")
async def app_info():
    """Get application information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "ai_model": settings.AI_MODEL,
        "debug": settings.DEBUG,
        "features": {
            "social_media": bool(settings.RAPIDAPI_KEY),
            "browser_automation": bool(settings.BROWSERLESS_API_KEY),
            "telegram": bool(settings.TELEGRAM_BOT_TOKEN),
            "youtube": bool(settings.YOUTUBE_API_KEY)
        }
    }
