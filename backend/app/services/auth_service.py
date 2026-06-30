import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
import jwt
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        # In-memory user storage (replace with database in production)
        self.users: Dict[str, Dict[str, Any]] = {}
        self._initialize_demo_user()

    def _initialize_demo_user(self):
        """Create a demo user for testing."""
        demo_user = {
            "id": "demo-user-id",
            "name": "Demo User",
            "email": "demo@example.com",
            "password_hash": pwd_context.hash("demo123"),
            "created_at": datetime.now()
        }
        self.users["demo@example.com"] = demo_user

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

    async def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        user = self.users.get(email)
        if not user:
            return None
        
        if not self.verify_password(password, user["password_hash"]):
            return None
        
        token = self.create_access_token(user["id"])
        
        return {
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "created_at": user["created_at"]
            }
        }

    async def register(self, name: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        if email in self.users:
            return None
        
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": self.hash_password(password),
            "created_at": datetime.now()
        }
        
        self.users[email] = user
        
        token = self.create_access_token(user_id)
        
        return {
            "token": token,
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "created_at": user["created_at"]
            }
        }

    async def reset_password(self, email: str) -> bool:
        """Send password reset email."""
        if email not in self.users:
            return False
        
        # In production, this would send an actual email
        # For demo, just return True
        return True

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        for user in self.users.values():
            if user["id"] == user_id:
                return {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "created_at": user["created_at"]
                }
        return None

# Singleton instance
auth_service = AuthService()
