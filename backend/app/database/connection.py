"""
Database Connection Manager for Neon DB
=======================================
Handles async connection pooling with asyncpg and SQLAlchemy
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool

from app.database.models import Base
from app.config import settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Singleton database manager for Neon DB connections
    Handles connection pooling, session management, and table creation
    """
    
    _instance: Optional["DatabaseManager"] = None
    _engine: Optional[AsyncEngine] = None
    _session_factory: Optional[async_sessionmaker[AsyncSession]] = None

    def __new__(cls) -> "DatabaseManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def engine(self) -> AsyncEngine:
        """Get or create async engine"""
        if self._engine is None:
            self._initialize_engine()
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create session factory"""
        if self._session_factory is None:
            self._initialize_engine()
        return self._session_factory

    def _initialize_engine(self) -> None:
        """Initialize async engine with Neon DB connection string"""
        database_url = settings.DATABASE_URL

        if not database_url:
            logger.warning("DATABASE_URL not set. Using SQLite fallback for development.")
            database_url = "sqlite+aiosqlite:///./dev.db"

        # Convert postgresql:// to postgresql+asyncpg:// for async support
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            # Add sslmode if not present
            if "sslmode" not in database_url:
                separator = "&" if "?" in database_url else "?"
                database_url = f"{database_url}{separator}sslmode=require"

        logger.info(f"Connecting to database...")

        # Create async engine with optimized pool settings
        self._engine = create_async_engine(
            database_url,
            echo=settings.DEBUG,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=3600,
            pool_pre_ping=True,  # Enable connection health checks
            connect_args={
                "server_settings": {
                    "application_name": "amkyawdev_agent"
                }
            } if "asyncpg" in database_url else {}
        )

        # Create session factory
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False
        )

        logger.info("Database engine initialized successfully")

    async def create_tables(self) -> None:
        """Create all tables in the database"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")

    async def drop_tables(self) -> None:
        """Drop all tables (use with caution!)"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.warning("All database tables dropped")

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Context manager for database sessions
        Automatically handles commit/rollback and cleanup
        """
        session: AsyncSession = self.session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Dependency injection generator for FastAPI
        Usage: async def endpoint(session: AsyncSession = Depends(get_db))
        """
        async with self.session() as session:
            yield session

    async def health_check(self) -> dict:
        """Check database connectivity"""
        try:
            async with self.session() as session:
                result = await session.execute("SELECT 1")
                result.scalar()
            return {"status": "healthy", "message": "Database connection OK"}
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

    async def close(self) -> None:
        """Close all database connections"""
        if self._engine:
            await self._engine.dispose()
            logger.info("Database connections closed")


# Global instance
db_manager = DatabaseManager()


# Convenience function for dependency injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database sessions"""
    return db_manager.get_session()
