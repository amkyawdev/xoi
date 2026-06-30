"""
Database initialization and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from contextlib import contextmanager
from typing import Generator
import os
from app.config import settings

# Sync engine (for migrations, CLI operations)
sync_engine = None
SyncSessionLocal = None

# Async engine (for FastAPI)
async_engine = None
AsyncSessionLocal = None


def init_database():
    """Initialize database connections"""
    global sync_engine, SyncSessionLocal, async_engine, AsyncSessionLocal
    
    database_url = os.getenv("DATABASE_URL") or settings.DATABASE_URL
    
    if database_url and "postgresql" in database_url:
        # Use sync engine for general operations
        sync_engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            echo=settings.DEBUG
        )
        SyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=sync_engine
        )
        
        # Use async engine for FastAPI
        async_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        async_engine = create_async_engine(
            async_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            echo=settings.DEBUG
        )
        AsyncSessionLocal = sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        return True
    return False


def get_sync_session() -> Generator[Session, None, None]:
    """Get sync database session"""
    if SyncSessionLocal:
        session = SyncSessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


@contextmanager
def get_sync_session_context():
    """Context manager for sync session"""
    if SyncSessionLocal:
        session = SyncSessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


async def get_async_session() -> Generator[AsyncSession, None, None]:
    """Get async database session for FastAPI"""
    if AsyncSessionLocal:
        async with AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise


def create_tables():
    """Create all database tables"""
    if sync_engine:
        from app.database.models.user import Base as UserBase
        from app.database.models.chat_history import Base as ChatBase
        
        UserBase.metadata.create_all(bind=sync_engine)
        ChatBase.metadata.create_all(bind=sync_engine)
        return True
    return False


def drop_tables():
    """Drop all database tables"""
    if sync_engine:
        from app.database.models.user import Base as UserBase
        from app.database.models.chat_history import Base as ChatBase
        
        ChatBase.metadata.drop_all(bind=sync_engine)
        UserBase.metadata.drop_all(bind=sync_engine)
        return True
    return False
