from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional
from pydantic import BaseModel
from app.api.models.response_models import SettingsResponse

router = APIRouter()

# In-memory settings storage (replace with database in production)
_user_settings = {
    "theme": "light",
    "language": "en",
    "notifications": True,
    "model": "gpt-4o",
    "temperature": 0.7
}

@router.get("/settings", response_model=SettingsResponse)
async def get_settings():
    return SettingsResponse(**_user_settings)

@router.put("/settings", response_model=SettingsResponse)
async def update_settings(
    theme: Optional[str] = Body(None),
    language: Optional[str] = Body(None),
    notifications: Optional[bool] = Body(None),
    model: Optional[str] = Body(None),
    temperature: Optional[float] = Body(None)
):
    global _user_settings
    
    if theme is not None:
        _user_settings["theme"] = theme
    if language is not None:
        _user_settings["language"] = language
    if notifications is not None:
        _user_settings["notifications"] = notifications
    if model is not None:
        _user_settings["model"] = model
    if temperature is not None:
        _user_settings["temperature"] = temperature
    
    return SettingsResponse(**_user_settings)
