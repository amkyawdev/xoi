"""
SQLAlchemy Models for Neon Database
====================================
Defines all database schemas using async SQLAlchemy 2.0
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all models"""
    pass


class User(Base):
    """User model for authentication and profile management"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, nullable=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    conversations: Mapped[List["Conversation"]] = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    cache_entries: Mapped[List["CacheEntry"]] = relationship("CacheEntry", back_populates="user", cascade="all, delete-orphan")
    user_states: Mapped[List["UserState"]] = relationship("UserState", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class Conversation(Base):
    """Conversation model for tracking chat sessions"""
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_conversations_user_created", "user_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, user_id={self.user_id})>"


class Message(Base):
    """Message model for storing conversation messages"""
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")

    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<Message(id={self.id}, role={self.role})>"


class CacheEntry(Base):
    """Cache model for storing API responses and computed data"""
    __tablename__ = "cache_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    cache_key: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    cache_value: Mapped[dict] = mapped_column(JSON, nullable=False)
    ttl_seconds: Mapped[int] = mapped_column(Integer, default=3600)  # Default 1 hour
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped[Optional["User"]] = relationship("User", back_populates="cache_entries")

    __table_args__ = (
        Index("ix_cache_entries_user_key", "user_id", "cache_key"),
    )

    def is_expired(self) -> bool:
        """Check if cache entry has expired"""
        if self.ttl_seconds is None:
            return False
        age = (datetime.utcnow() - self.created_at).total_seconds()
        return age > self.ttl_seconds

    def __repr__(self) -> str:
        return f"<CacheEntry(id={self.id}, key={self.cache_key})>"


class UserState(Base):
    """User state model for tracking conversation context and temporary data"""
    __tablename__ = "user_states"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    state_key: Mapped[str] = mapped_column(String(100), nullable=False)
    state_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="user_states")

    __table_args__ = (
        Index("ix_user_states_user_key", "user_id", "state_key"),
    )

    def is_expired(self) -> bool:
        """Check if state has expired"""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def __repr__(self) -> str:
        return f"<UserState(id={self.id}, user_id={self.user_id}, key={self.state_key})>"


class WebhookLog(Base):
    """Webhook log model for tracking incoming webhooks"""
    __tablename__ = "webhook_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    event_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    headers: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, processed, failed
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    processed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("ix_webhook_logs_source_created", "source", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<WebhookLog(id={self.id}, source={self.source})>"
