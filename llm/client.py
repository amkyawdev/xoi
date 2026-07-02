"""LLM client for interacting with language models"""

import os
from typing import Any, AsyncIterator

from llm.models import ModelConfig, Message
from llm.providers.openrouter import OpenRouterProvider
from llm.providers.fallback import FallbackProvider


class LLMClient:
    """Client for LLM interactions"""
    
    def __init__(
        self,
        api_key: str | None = None,
        default_model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 4096
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY", "")
        self.default_model = default_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize providers
        self.providers: dict[str, Any] = {
            "openrouter": OpenRouterProvider(api_key=self.api_key),
            "fallback": FallbackProvider()
        }
    
    async def chat(
        self,
        messages: list[Message],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stream: bool = False
    ) -> dict[str, Any] | AsyncIterator[str]:
        """Send chat completion request"""
        model = model or self.default_model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens
        
        # Route to appropriate provider
        provider = self._get_provider(model)
        
        if stream:
            return self._stream_response(provider, model, messages, temperature, max_tokens)
        
        return await provider.chat(messages, model, temperature, max_tokens)
    
    async def _stream_response(
        self,
        provider: Any,
        model: str,
        messages: list[Message],
        temperature: float,
        max_tokens: int
    ) -> AsyncIterator[str]:
        """Stream response from provider"""
        async for chunk in provider.stream(messages, model, temperature, max_tokens):
            yield chunk
    
    def _get_provider(self, model: str) -> Any:
        """Get provider for model"""
        if "openrouter" in model or "/" in model:
            return self.providers["openrouter"]
        return self.providers["openrouter"]  # Default to openrouter
    
    def list_models(self) -> list[ModelConfig]:
        """List available models"""
        return [
            ModelConfig(name="gpt-4", provider="openai", context_length=8192),
            ModelConfig(name="gpt-3.5-turbo", provider="openai", context_length=16385),
            ModelConfig(name="claude-3-opus", provider="anthropic", context_length=200000),
            ModelConfig(name="mixtral-8x7b", provider="openrouter", context_length=32768),
            ModelConfig(name="llama-3-70b", provider="openrouter", context_length=8192),
        ]


# Global client instance
_client: LLMClient | None = None


def get_client() -> LLMClient:
    """Get or create global LLM client"""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
