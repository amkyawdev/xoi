"""Application settings"""

import os
from typing import Any
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    app_name: str = "web-agent-platform"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # API Keys
    openai_api_key: str = ""
    openrouter_api_key: str = ""
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/webagent"
    redis_url: str = "redis://localhost:6379/0"
    chroma_db_path: str = "./storage/vectors"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    max_request_size: int = 10485760
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    # Crawler
    max_crawl_depth: int = 5
    crawl_timeout_seconds: int = 30
    max_concurrent_crawls: int = 10
    
    # LLM (FREE MODELS - No cost!)
    default_model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"
    fallback_model: str = "qwen/qwen3-coder:free"
    temperature: float = 0.7
    max_tokens: int = 4096
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    enable_tracing: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings
settings = Settings()
