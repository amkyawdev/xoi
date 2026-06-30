"""
Neon PostgreSQL Connection Manager
"""
import os
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

Base = declarative_base()

class NeonClient:
    """Manages Neon PostgreSQL database connections"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
        self._connect()
    
    def _connect(self):
        """Create database connection"""
        database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
        
        if database_url:
            try:
                self.engine = create_engine(
                    database_url,
                    pool_pre_ping=True,
                    pool_size=5,
                    max_overflow=10
                )
                self.SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=self.engine
                )
            except Exception as e:
                print(f"Database connection error: {e}")
                self.engine = None
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if self.SessionLocal:
            return self.SessionLocal()
        return None
    
    def create_tables(self):
        """Create all tables"""
        if self.engine:
            Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables"""
        if self.engine:
            Base.metadata.drop_all(bind=self.engine)

# Singleton instance
neon_client = NeonClient()
