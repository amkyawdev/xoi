"""SQLite database"""

import aiosqlite
from typing import Any


class SQLiteDB:
    """SQLite database wrapper"""
    
    def __init__(self, db_path: str = "./storage/database.db"):
        self.db_path = db_path
    
    async def connect(self) -> aiosqlite.Connection:
        """Connect to database"""
        return await aiosqlite.connect(self.db_path)
    
    async def execute(self, query: str, params: tuple = ()) -> None:
        """Execute query"""
        async with await self.connect() as db:
            await db.execute(query, params)
            await db.commit()
    
    async def fetch_one(self, query: str, params: tuple = ()) -> dict[str, Any] | None:
        """Fetch one row"""
        async with await self.connect() as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params)
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    async def fetch_all(self, query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Fetch all rows"""
        async with await self.connect() as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def init_schema(self) -> None:
        """Initialize database schema"""
        await self.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        await self.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
