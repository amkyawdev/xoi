"""
Cache Service
=============
Handles cache operations for the controller
"""

import json
import hashlib
import logging
from typing import Optional, Any, Dict
from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import CacheEntry, UserState
from app.database.connection import db_manager

logger = logging.getLogger(__name__)


class CacheService:
    """
    Service for managing cache entries in Neon DB
    Provides TTL-based caching for API responses and computed data
    """
    
    @staticmethod
    def generate_key(*args, prefix: str = "cache") -> str:
        """Generate a unique cache key from arguments"""
        key_parts = [prefix] + [str(arg) for arg in args]
        key_string = ":".join(key_parts)
        # Hash if key is too long
        if len(key_string) > 450:
            hash_part = hashlib.md5(key_string.encode()).hexdigest()
            return f"{prefix}:{hash_part}"
        return key_string

    async def get(
        self,
        user_id: Optional[int],
        cache_key: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached value by key
        
        Args:
            user_id: Optional user ID for user-specific caching
            cache_key: Cache key to lookup
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        async with db_manager.session() as session:
            query = select(CacheEntry).where(
                CacheEntry.cache_key == cache_key,
                CacheEntry.user_id == user_id
            )
            result = await session.execute(query)
            entry = result.scalar_one_or_none()
            
            if entry is None:
                logger.debug(f"Cache miss: {cache_key}")
                return None
            
            # Check expiration
            if entry.is_expired():
                logger.debug(f"Cache expired: {cache_key}")
                await session.delete(entry)
                return None
            
            logger.debug(f"Cache hit: {cache_key}")
            return entry.cache_value

    async def set(
        self,
        user_id: Optional[int],
        cache_key: str,
        value: Dict[str, Any],
        ttl_seconds: int = 3600
    ) -> bool:
        """
        Set cache value with TTL
        
        Args:
            user_id: Optional user ID for user-specific caching
            cache_key: Cache key
            value: Value to cache (must be JSON-serializable)
            ttl_seconds: Time-to-live in seconds (default: 1 hour)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            async with db_manager.session() as session:
                # Check for existing entry
                query = select(CacheEntry).where(
                    CacheEntry.cache_key == cache_key,
                    CacheEntry.user_id == user_id
                )
                result = await session.execute(query)
                existing = result.scalar_one_or_none()
                
                if existing:
                    # Update existing entry
                    existing.cache_value = value
                    existing.ttl_seconds = ttl_seconds
                    existing.updated_at = datetime.utcnow()
                else:
                    # Create new entry
                    entry = CacheEntry(
                        user_id=user_id,
                        cache_key=cache_key,
                        cache_value=value,
                        ttl_seconds=ttl_seconds
                    )
                    session.add(entry)
                
                await session.commit()
                logger.debug(f"Cache set: {cache_key} (TTL: {ttl_seconds}s)")
                return True
                
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(
        self,
        user_id: Optional[int],
        cache_key: str
    ) -> bool:
        """Delete a cache entry"""
        try:
            async with db_manager.session() as session:
                await session.execute(
                    delete(CacheEntry).where(
                        CacheEntry.cache_key == cache_key,
                        CacheEntry.user_id == user_id
                    )
                )
                await session.commit()
                logger.debug(f"Cache deleted: {cache_key}")
                return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    async def clear_user_cache(self, user_id: int) -> int:
        """Clear all cache entries for a user"""
        try:
            async with db_manager.session() as session:
                result = await session.execute(
                    delete(CacheEntry).where(CacheEntry.user_id == user_id)
                )
                await session.commit()
                count = result.rowcount
                logger.info(f"Cleared {count} cache entries for user {user_id}")
                return count
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0


class StateService:
    """
    Service for managing user state in Neon DB
    Handles conversation context and temporary state data
    """
    
    async def get_state(
        self,
        user_id: int,
        state_key: str
    ) -> Optional[Dict[str, Any]]:
        """Get user state by key"""
        async with db_manager.session() as session:
            query = select(UserState).where(
                UserState.user_id == user_id,
                UserState.state_key == state_key
            )
            result = await session.execute(query)
            state = result.scalar_one_or_none()
            
            if state is None:
                return None
            
            # Check expiration
            if state.is_expired():
                await session.delete(state)
                return None
            
            return state.state_data

    async def set_state(
        self,
        user_id: int,
        state_key: str,
        state_data: Dict[str, Any],
        expires_in_seconds: Optional[int] = None
    ) -> bool:
        """Set user state with optional expiration"""
        try:
            async with db_manager.session() as session:
                from datetime import timedelta
                
                query = select(UserState).where(
                    UserState.user_id == user_id,
                    UserState.state_key == state_key
                )
                result = await session.execute(query)
                existing = result.scalar_one_or_none()
                
                expires_at = None
                if expires_in_seconds:
                    expires_at = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
                
                if existing:
                    existing.state_data = state_data
                    existing.expires_at = expires_at
                    existing.updated_at = datetime.utcnow()
                else:
                    state = UserState(
                        user_id=user_id,
                        state_key=state_key,
                        state_data=state_data,
                        expires_at=expires_at
                    )
                    session.add(state)
                
                await session.commit()
                return True
                
        except Exception as e:
            logger.error(f"State set error: {e}")
            return False

    async def delete_state(self, user_id: int, state_key: str) -> bool:
        """Delete user state"""
        try:
            async with db_manager.session() as session:
                await session.execute(
                    delete(UserState).where(
                        UserState.user_id == user_id,
                        UserState.state_key == state_key
                    )
                )
                await session.commit()
                return True
        except Exception as e:
            logger.error(f"State delete error: {e}")
            return False

    async def clear_expired_states(self) -> int:
        """Clear all expired user states"""
        try:
            async with db_manager.session() as session:
                result = await session.execute(
                    delete(UserState).where(
                        UserState.expires_at < datetime.utcnow()
                    )
                )
                await session.commit()
                count = result.rowcount
                if count > 0:
                    logger.info(f"Cleared {count} expired states")
                return count
        except Exception as e:
            logger.error(f"Expired states clear error: {e}")
            return 0


# Singleton instances
cache_service = CacheService()
state_service = StateService()
