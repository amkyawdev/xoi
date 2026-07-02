"""Rate limiting"""

import time
from collections import defaultdict
from typing import Callable

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: dict[str, list[float]] = defaultdict(list)
    
    def _cleanup_old_requests(self, key: str) -> None:
        """Remove old requests from tracking"""
        now = time.time()
        cutoff = now - 60  # 1 minute ago
        self.requests[key] = [t for t in self.requests[key] if t > cutoff]
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        self._cleanup_old_requests(key)
        
        if len(self.requests[key]) >= self.requests_per_minute:
            return False
        
        self.requests[key].append(time.time())
        return True
    
    def get_remaining(self, key: str) -> int:
        """Get remaining requests"""
        self._cleanup_old_requests(key)
        return max(0, self.requests_per_minute - len(self.requests[key]))
    
    def reset(self, key: str) -> None:
        """Reset rate limit for key"""
        if key in self.requests:
            del self.requests[key]


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute)
    
    async def dispatch(self, request: Request, call_next: Callable):
        """Process request with rate limiting"""
        # Get client identifier
        client_ip = request.client.host if request.client else "unknown"
        key = f"{client_ip}:{request.url.path}"
        
        if not self.limiter.is_allowed(key):
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(self.limiter.get_remaining(key))
        return response
