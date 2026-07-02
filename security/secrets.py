"""Secrets management"""

import os
from typing import Any


class SecretsManager:
    """Manage application secrets"""
    
    def __init__(self):
        self._cache: dict[str, str] = {}
    
    def get(self, key: str) -> str | None:
        """Get secret value"""
        if key in self._cache:
            return self._cache[key]
        
        # Try environment variable
        value = os.getenv(key)
        if value:
            self._cache[key] = value
            return value
        
        return None
    
    def set(self, key: str, value: str) -> None:
        """Set secret value"""
        self._cache[key] = value
    
    def get_required(self, key: str) -> str:
        """Get required secret, raise if missing"""
        value = self.get(key)
        if value is None:
            raise ValueError(f"Required secret '{key}' is not set")
        return value


# Global secrets manager
secrets = SecretsManager()
