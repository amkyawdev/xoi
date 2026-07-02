"""In-memory cache"""

import time
from typing import Any


class MemoryCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self._cache: dict[str, tuple[Any, float]] = {}
    
    def get(self, key: str) -> Any | None:
        """Get value from cache"""
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        
        if expiry < time.time():
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        ttl = ttl if ttl is not None else self.default_ttl
        expiry = time.time() + ttl
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache"""
        self._cache.clear()
    
    def cleanup(self) -> int:
        """Remove expired entries"""
        now = time.time()
        expired = [k for k, (_, exp) in self._cache.items() if exp < now]
        for key in expired:
            del self._cache[key]
        return len(expired)


# Global cache
cache = MemoryCache()
