"""Encryption utilities"""

import base64
import os
from typing import Any

from cryptography.fernet import Fernet
from passlib.context import CryptContext


class EncryptionManager:
    """Manage data encryption"""
    
    def __init__(self, key: bytes | None = None):
        if key is None:
            key = os.getenv("ENCRYPTION_KEY", "").encode()
            if not key:
                key = Fernet.generate_key()
        
        self.cipher = Fernet(key)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data"""
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data"""
        decoded = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()
    
    def hash_password(self, password: str) -> str:
        """Hash password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password"""
        return self.pwd_context.verify(plain_password, hashed_password)


# Global encryption manager
encryption = EncryptionManager()
