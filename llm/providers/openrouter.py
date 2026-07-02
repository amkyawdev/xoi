"""OpenRouter provider implementation"""

import os
from typing import Any, AsyncIterator

import httpx

from llm.models import Message


class OpenRouterProvider:
    """Provider for OpenRouter API"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            timeout=60.0
        )
    
    async def chat(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> dict[str, Any]:
        """Send chat completion request"""
        payload = {
            "model": model,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = await self.client.post("/chat/completions", json=payload)
        response.raise_for_status()
        return response.json()
    
    async def stream(
        self,
        messages: list[Message],
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> AsyncIterator[str]:
        """Stream chat completion"""
        payload = {
            "model": model,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True
        }
        
        async with self.client.stream("POST", "/chat/completions", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    if line.startswith("data: [DONE]"):
                        break
                    # Parse SSE data
                    import json
                    try:
                        data = json.loads(line[6:])
                        if content := data.get("choices", [{}])[0].get("delta", {}).get("content"):
                            yield content
                    except json.JSONDecodeError:
                        continue
    
    async def list_models(self) -> list[dict[str, Any]]:
        """List available models"""
        response = await self.client.get("/models")
        response.raise_for_status()
        return response.json().get("data", [])
    
    async def close(self) -> None:
        """Close the client"""
        await self.client.aclose()
