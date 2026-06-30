import os
import secrets
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
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # AI Service (Hugging Face - Primary)
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    HF_INFERENCE_ENDPOINT: str = os.getenv("HF_INFERENCE_ENDPOINT", "https://api-inference.huggingface.co/models")
    AI_MODEL: str = os.getenv("AI_MODEL", "Qwen/Qwen2.5-7B-Instruct")
    AI_TEMPERATURE: float = 0.6
    AI_MAX_TOKENS: int = 4096

    # AI Service (Groq - Backup)
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate SECRET_KEY in production
        if not self.DEBUG and not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production (non-debug mode)")
        # Auto-generate SECRET_KEY if not set in debug mode
        if not self.SECRET_KEY:
            import secrets
            self.SECRET_KEY = secrets.token_urlsafe(32)
            import logging
            logging.getLogger(__name__).warning("SECRET_KEY auto-generated. Set SECRET_KEY in environment for production!")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
