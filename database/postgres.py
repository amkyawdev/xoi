"""PostgreSQL database"""

from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime, select


Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")


class ChatHistory(Base):
    """Chat history model"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")


class PostgresDB:
    """PostgreSQL database wrapper"""
    
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url, echo=False)
        self.session_maker = async_sessionmaker(self.engine, class_=AsyncSession)
    
    async def create_tables(self) -> None:
        """Create all tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def add_user(self, username: str, email: str, password_hash: str) -> User:
        """Add new user"""
        async with self.session_maker() as session:
            user = User(username=username, email=email, password_hash=password_hash)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
    
    async def get_user(self, username: str) -> User | None:
        """Get user by username"""
        async with self.session_maker() as session:
            result = await session.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()
    
    async def add_chat_message(self, session_id: str, role: str, content: str) -> ChatHistory:
        """Add chat message"""
        async with self.session_maker() as session:
            message = ChatHistory(session_id=session_id, role=role, content=content)
            session.add(message)
            await session.commit()
            await session.refresh(message)
            return message
