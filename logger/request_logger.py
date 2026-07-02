"""Request logging middleware"""

import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLogger(BaseHTTPMiddleware):
    """Log all HTTP requests"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process request and log"""
        from logger.logger import get_logger
        
        logger = get_logger("request")
        start_time = time.time()
        
        # Log request
        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
            client=request.client.host if request.client else None
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2)
        )
        
        return response
