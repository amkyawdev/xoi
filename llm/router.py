"""LLM router for selecting appropriate model"""

from typing import Any

from llm.models import ModelConfig


class LLM Router:
    """Routes requests to appropriate LLM based on requirements"""
    
    def __init__(self):
        self.models: dict[str, ModelConfig] = {
            "gpt-4": ModelConfig(
                name="gpt-4",
                provider="openai",
                context_length=8192,
                capabilities=["chat", "function_calling", "vision"]
            ),
            "gpt-3.5-turbo": ModelConfig(
                name="gpt-3.5-turbo",
                provider="openai",
                context_length=16385,
                capabilities=["chat", "function_calling"]
            ),
            "claude-3-opus": ModelConfig(
                name="claude-3-opus",
                provider="anthropic",
                context_length=200000,
                capabilities=["chat", "vision", "long_context"]
            ),
            "mixtral-8x7b": ModelConfig(
                name="mixtral-8x7b",
                provider="openrouter",
                context_length=32768,
                capabilities=["chat"]
            ),
        }
    
    def select_model(
        self,
        task_type: str | None = None,
        context_length: int | None = None,
        capabilities: list[str] | None = None,
        prefer_fast: bool = False
    ) -> str:
        """Select appropriate model based on requirements"""
        candidates = list(self.models.values())
        
        # Filter by capabilities
        if capabilities:
            candidates = [
                m for m in candidates
                if all(cap in m.capabilities for cap in capabilities)
            ]
        
        # Filter by context length
        if context_length:
            candidates = [m for m in candidates if m.context_length >= context_length]
        
        if not candidates:
            return "gpt-3.5-turbo"  # Default fallback
        
        # Select based on preferences
        if prefer_fast:
            return min(candidates, key=lambda m: m.name).name
        
        return candidates[0].name
    
    def get_model(self, name: str) -> ModelConfig | None:
        """Get model configuration by name"""
        return self.models.get(name)
    
    def add_model(self, config: ModelConfig) -> None:
        """Add a new model configuration"""
        self.models[config.name] = config
    
    def list_models(self) -> list[ModelConfig]:
        """List all available models"""
        return list(self.models.values())


# Global router
_router: LLM Router | None = None


def get_router() -> LLMRouter:
    """Get or create global LLM router"""
    global _router
    if _router is None:
        _router = LLM Router()
    return _router
