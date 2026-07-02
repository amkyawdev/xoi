"""Cache manager"""

from typing import Any

from cache.memory_cache import MemoryCache, cache as memory_cache
from cache.redis_cache import RedisCache


class CacheManager:
    """Unified cache manager"""
    
    def __init__(self, use_redis: bool = False, redis_url: str = "redis://localhost:6379/0"):
        self.use_redis = use_redis
        self.memory = memory_cache
        
        if use_redis:
            self.redis = RedisCache(url=redis_url)
    
    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        if self.use_redis:
            return await self.redis.get(key)
        return self.memory.get(key)
    
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        if self.use_redis:
            await self.redis.set(key, value, ttl)
        else:
            self.memory.set(key, value, ttl)
    
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        if self.use_redis:
            await self.redis.delete(key)
        else:
            self.memory.delete(key)
    
    async def clear(self) -> None:
        """Clear all cache"""
        if self.use_redis:
            await self.redis.clear()
        else:
            self.memory.clear()
