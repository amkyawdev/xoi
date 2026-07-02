"""FastAPI server"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import ai, chat, crawler, search, health, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager"""
    # Startup
    print("Starting API server...")
    yield
    # Shutdown
    print("Shutting down API server...")


app = FastAPI(
    title="Web Agent Platform API",
    description="AI agent platform for web automation and crawling",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(crawler.router, prefix="/api/crawler", tags=["Crawler"])
app.include_router(search.router, prefix="/api/search", tags=["Search"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Web Agent Platform API", "version": "0.1.0"}


def main():
    """Run the server"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
