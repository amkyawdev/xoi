"""Fallback LLM provider"""

from typing import Any, AsyncIterator

from llm.models import Message


class FallbackProvider:
    """Fallback provider for when primary is unavailable"""
    
    async def chat(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> dict[str, Any]:
        """Return mock response for testing"""
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": "This is a fallback response. Configure an API key for actual responses."
                },
                "finish_reason": "stop"
            }],
            "model": model
        }
    
    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> AsyncIterator[str]:
        """Yield mock streaming response"""
        response = "This is a fallback response. Configure an API key for actual responses."
        for char in response:
            yield char
