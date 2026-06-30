from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChatResponse(BaseModel):
    message: str
    conversation_id: Optional[str] = ""
    created_at: datetime = datetime.now()

class AuthResponse(BaseModel):
    token: str
    user: "UserResponse"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime

class SettingsResponse(BaseModel):
    theme: str = "light"
    language: str = "en"
    notifications: bool = True
    model: str = "gpt-4o"
    temperature: float = 0.7

class HistoryResponse(BaseModel):
    conversations: List["ConversationResponse"]
    total: int
    limit: int
    offset: int

class ConversationResponse(BaseModel):
    id: str
    messages: List["MessageResponse"]
    created_at: datetime
    updated_at: datetime

class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    content_type: str
    url: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# Update forward references
AuthResponse.model_rebuild()
HistoryResponse.model_rebuild()
ConversationResponse.model_rebuild()
