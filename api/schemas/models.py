"""Pydantic models for API"""

from typing import Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request"""
    messages: list[Message]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat response"""
    choices: list[dict[str, Any]]
    model: str
    usage: dict[str, int] | None = None


class CrawlRequest(BaseModel):
    """Crawl request"""
    url: str = Field(..., description="URL to crawl")
    depth: int = Field(2, description="Crawl depth")
    max_pages: int = Field(100, description="Maximum pages to crawl")


class CrawlResponse(BaseModel):
    """Crawl response"""
    url: str
    status: int
    content: str
    links: list[str]


class SearchRequest(BaseModel):
    """Search request"""
    query: str
    engine: str = "ddg"
    limit: int = 10


class SearchResult(BaseModel):
    """Search result"""
    title: str
    url: str
    snippet: str


class SearchResponse(BaseModel):
    """Search response"""
    results: list[SearchResult]
    total: int


class HealthResponse(BaseModel):
    """Health response"""
    status: str
    version: str


class SettingsUpdate(BaseModel):
    """Settings update"""
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
