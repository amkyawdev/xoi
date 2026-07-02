"""Error logging"""

import traceback
from typing import Any


class ErrorLogger:
    """Handles error logging"""
    
    def __init__(self):
        from logger.logger import get_logger
        self.logger = get_logger("error")
    
    def log_exception(self, exc: Exception, context: dict[str, Any] | None = None) -> None:
        """Log exception with context"""
        self.logger.error(
            "exception_occurred",
            error_type=type(exc).__name__,
            error_message=str(exc),
            traceback=traceback.format_exc(),
            **(context or {})
        )
    
    def log_error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error("error", message=message, **kwargs)


# Global error logger
error_logger = ErrorLogger()
