"""Redis cache"""

import json
from typing import Any

import redis.asyncio as redis


class RedisCache:
    """Redis-based cache"""
    
    def __init__(self, url: str = "redis://localhost:6379/0", default_ttl: int = 300):
        self.url = url
        self.default_ttl = default_ttl
        self._client: redis.Redis | None = None
    
    async def connect(self) -> redis.Redis:
        """Connect to Redis"""
        if self._client is None:
            self._client = redis.from_url(self.url, decode_responses=True)
        return self._client
    
    async def get(self, key: str) -> Any | None:
        """Get value from cache"""
        client = await self.connect()
        value = await client.get(key)
        
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        """Set value in cache"""
        client = await self.connect()
        ttl = ttl or self.default_ttl
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await client.set(key, value, ex=ttl)
    
    async def delete(self, key: str) -> None:
        """Delete value from cache"""
        client = await self.connect()
        await client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        client = await self.connect()
        return await client.exists(key) > 0
    
    async def clear(self) -> None:
        """Clear all cache"""
        client = await self.connect()
        await client.flushdb()
