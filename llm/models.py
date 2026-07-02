"""LLM models and schemas"""

from typing import Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Chat message"""
    role: str = Field(..., description="Role: system, user, or assistant")
    content: str = Field(..., description="Message content")
    name: str | None = Field(None, description="Name of the sender")


class ModelConfig(BaseModel):
    """Model configuration"""
    name: str
    provider: str
    context_length: int
    capabilities: list[str] = []
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0


class ChatRequest(BaseModel):
    """Chat completion request"""
    messages: list[Message]
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 4096
    stream: bool = False


class ChatResponse(BaseModel):
    """Chat completion response"""
    choices: list[dict[str, Any]]
    model: str
    usage: dict[str, int] | None = None
