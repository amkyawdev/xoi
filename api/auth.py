"""Authentication utilities"""

import os
from datetime import datetime, timedelta
from typing import Any

from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jose import JWTError, jwt


ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")


security = HTTPBearer()


def create_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1440)  # 24 hours
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict[str, Any]:
    """Verify JWT token"""
    return decode_token(credentials.credentials)


def get_current_user(token_data: dict[str, Any] = Security(verify_token)) -> dict[str, Any]:
    """Get current user from token"""
    return token_data
