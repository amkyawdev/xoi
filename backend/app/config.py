import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Amkyaw AI Agent"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/amkyaw")

    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # AI Service (Groq - Primary)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    AI_MODEL: str = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
    AI_TEMPERATURE: float = 0.6
    AI_MAX_TOKENS: int = 4096

    # AI Service (OpenAI - Backup)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # RapidAPI (optional)
    RAPIDAPI_KEY: str = os.getenv("RAPIDAPI_KEY", "")

    # YouTube API (optional)
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")

    # Browserless MCP (optional)
    BROWSERLESS_API_KEY: str = os.getenv("BROWSERLESS_API_KEY", "")

    # Telegram (optional)
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")

    # File uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
