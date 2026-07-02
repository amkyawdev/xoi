"""JWT utilities"""

from datetime import datetime, timedelta
from typing import Any

from jose import jwt, JWTError


class JWTManager:
    """Manage JWT tokens"""
    
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    def create_token(self, data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        """Create JWT token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
        to_encode.update({"exp": expire, "iat": datetime.utcnow()})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict[str, Any]:
        """Decode JWT token"""
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def verify_token(self, token: str) -> bool:
        """Verify token is valid"""
        try:
            self.decode_token(token)
            return True
        except ValueError:
            return False
