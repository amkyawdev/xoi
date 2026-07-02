"""Settings routes"""

from fastapi import APIRouter, HTTPException

from api.schemas import SettingsUpdate


router = APIRouter()

# In-memory settings (would be in database in production)
settings = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 4096
}


@router.get("")
async def get_settings() -> dict:
    """Get current settings"""
    return settings


@router.post("")
async def update_settings(update: SettingsUpdate) -> dict:
    """Update settings"""
    settings.update(update.model_dump(exclude_none=True))
    return settings


@router.get("/models")
async def list_models() -> list[dict]:
    """List available models"""
    return [
        {"name": "gpt-4", "provider": "openai"},
        {"name": "gpt-3.5-turbo", "provider": "openai"},
        {"name": "claude-3-opus", "provider": "anthropic"},
        {"name": "mixtral-8x7b", "provider": "openrouter"}
    ]
