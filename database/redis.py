"""Redis cache/database"""

import json
from typing import Any

import redis.asyncio as redis


class RedisDB:
    """Redis database wrapper"""
    
    def __init__(self, url: str = "redis://localhost:6379/0"):
        self.url = url
        self._client: redis.Redis | None = None
    
    async def connect(self) -> redis.Redis:
        """Connect to Redis"""
        if self._client is None:
            self._client = redis.from_url(self.url, decode_responses=True)
        return self._client
    
    async def get(self, key: str) -> Any | None:
        """Get value"""
        client = await self.connect()
        value = await client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    async def set(self, key: str, value: Any, expire: int | None = None) -> None:
        """Set value with optional expiration"""
        client = await self.connect()
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        await client.set(key, value, ex=expire)
    
    async def delete(self, key: str) -> None:
        """Delete key"""
        client = await self.connect()
        await client.delete(key)
    
    async def exists(self, key: str) -> bool:
        """Check if key exists"""
        client = await self.connect()
        return await client.exists(key) > 0
    
    async def incr(self, key: str) -> int:
        """Increment value"""
        client = await self.connect()
        return await client.incr(key)
    
    async def expire(self, key: str, seconds: int) -> None:
        """Set expiration"""
        client = await self.connect()
        await client.expire(key, seconds)
