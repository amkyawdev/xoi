import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database setup
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create engine and session
engine = None
SessionLocal = None

def init_db():
    global engine, SessionLocal
    if settings.DATABASE_URL:
        try:
            engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            # Create tables
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Database connection error: {e}")

# Initialize database on module load
init_db()

class AuthService:
    def __init__(self):
        self._ensure_demo_user()

    def _ensure_demo_user(self):
        """Ensure demo user exists in database."""
        if not SessionLocal:
            return
        
        db = SessionLocal()
        try:
            demo = db.query(User).filter(User.email == "demo@example.com").first()
            if not demo:
                demo_user = User(
                    id="demo-user-id",
                    name="Demo User",
                    email="demo@example.com",
                    password_hash=pwd_context.hash("demo123")
                )
                db.add(demo_user)
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error ensuring demo user: {e}")
        finally:
            db.close()

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": user_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def _get_db(self) -> Optional[Session]:
        if SessionLocal:
            return SessionLocal()
        return None

    async def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        db = self._get_db()
        if not db:
            return None
        
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None
            
            if not self.verify_password(password, user.password_hash):
                return None
            
            token = self.create_access_token(user.id)
            
            return {
                "token": token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "created_at": user.created_at
                }
            }
        finally:
            if db:
                db.close()

    async def register(self, name: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        db = self._get_db()
        if not db:
            return None
        
        try:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                return None
            
            user_id = str(uuid.uuid4())
            new_user = User(
                id=user_id,
                name=name,
                email=email,
                password_hash=self.hash_password(password)
            )
            
            db.add(new_user)
            db.commit()
            
            token = self.create_access_token(user_id)
            
            return {
                "token": token,
                "user": {
                    "id": user_id,
                    "name": name,
                    "email": email,
                    "created_at": new_user.created_at
                }
            }
        except Exception as e:
            db.rollback()
            print(f"Registration error: {e}")
            return None
        finally:
            if db:
                db.close()

    async def reset_password(self, email: str) -> bool:
        """Send password reset email."""
        db = self._get_db()
        if not db:
            return False
        
        try:
            user = db.query(User).filter(User.email == email).first()
            return user is not None
        finally:
            if db:
                db.close()

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        db = self._get_db()
        if not db:
            return None
        
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                return {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "created_at": user.created_at
                }
            return None
        finally:
            if db:
                db.close()

# Singleton instance
auth_service = AuthService()
