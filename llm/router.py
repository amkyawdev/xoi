"""LLM router for selecting appropriate model"""

import json
from pathlib import Path
from typing import Any

from llm.models import ModelConfig


class LLM Router:
    """Routes requests to appropriate LLM based on requirements"""
    
    def __init__(self, models_file: str | None = None):
        self.models: dict[str, ModelConfig] = {}
        
        # Load models from JSON config
        if models_file is None:
            models_file = Path(__file__).parent.parent / "config" / "models.json"
        
        if Path(models_file).exists():
            with open(models_file) as f:
                data = json.load(f)
                for m in data.get("models", []):
                    config = ModelConfig(
                        name=m["name"],
                        provider=m["provider"],
                        context_length=m.get("context_length", 8192),
                        capabilities=m.get("capabilities", ["chat"]),
                        cost_per_1k_input=m.get("cost_per_1k_input", 0),
                        cost_per_1k_output=m.get("cost_per_1k_output", 0)
                    )
                    self.models[config.name] = config
        else:
            # Fallback to default free models
            self._set_default_models()
    
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
            return "openrouter/free"  # Default fallback (free)
        
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
_router: "LLMRouter" | None = None


def get_router() -> "LLMRouter":
    """Get or create global LLM router"""
    global _router
    if _router is None:
        _router = LLM Router()
    return _router
