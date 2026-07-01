"""
Error Handler Middleware
========================
Centralized error handling with Telegram notifications
"""

import logging
import traceback
from typing import Optional, Callable, Any, Dict
from datetime import datetime
from enum import Enum

from telegram import Bot
from telegram.error import TelegramError

from app.config import settings

logger = logging.getLogger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification"""
    DATABASE_ERROR = "database_error"
    BROWSERLESS_ERROR = "browserless_error"
    TELEGRAM_ERROR = "telegram_error"
    VALIDATION_ERROR = "validation_error"
    TIMEOUT_ERROR = "timeout_error"
    NETWORK_ERROR = "network_error"
    UNKNOWN_ERROR = "unknown_error"


class AgenticError(Exception):
    """Base exception for agentic workflow errors"""
    
    def __init__(
        self,
        message: str,
        category: ErrorCategory = ErrorCategory.UNKNOWN_ERROR,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None,
        retry_after: Optional[int] = None
    ):
        super().__init__(message)
        self.message = message
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.retry_after = retry_after
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.message,
            "category": self.category.value,
            "severity": self.severity.value,
            "details": self.details,
            "retry_after": self.retry_after,
            "timestamp": self.timestamp.isoformat()
        }


class DatabaseError(AgenticError):
    """Database-related errors"""
    def __init__(self, message: str, details: Optional[Dict] = None, retry_after: int = 30):
        super().__init__(
            message=message,
            category=ErrorCategory.DATABASE_ERROR,
            severity=ErrorSeverity.HIGH,
            details=details,
            retry_after=retry_after
        )


class BrowserlessError(AgenticError):
    """Browserless API errors"""
    def __init__(self, message: str, details: Optional[Dict] = None, retry_after: int = 60):
        super().__init__(
            message=message,
            category=ErrorCategory.BROWSERLESS_ERROR,
            severity=ErrorSeverity.MEDIUM,
            details=details,
            retry_after=retry_after
        )


class TimeoutError(AgenticError):
    """Timeout errors"""
    def __init__(self, message: str, details: Optional[Dict] = None, retry_after: int = 120):
        super().__init__(
            message=message,
            category=ErrorCategory.TIMEOUT_ERROR,
            severity=ErrorSeverity.MEDIUM,
            details=details,
            retry_after=retry_after
        )


class ErrorHandler:
    """
    Centralized error handler with Telegram notification support
    """
    
    def __init__(self, telegram_bot: Optional[Bot] = None):
        self.telegram_bot = telegram_bot
        self._notification_chat_id: Optional[str] = None
        self.error_log: list = []
        self.max_log_size = 1000

    def set_notification_target(self, chat_id: str) -> None:
        """Set Telegram chat ID for error notifications"""
        self._notification_chat_id = chat_id

    def set_telegram_bot(self, bot: Bot) -> None:
        """Set Telegram bot for notifications"""
        self.telegram_bot = bot

    async def notify_user(
        self,
        error: AgenticError,
        user_id: Optional[int] = None,
        context: Optional[str] = None
    ) -> bool:
        """
        Send error notification to user via Telegram
        
        Args:
            error: The error to notify about
            user_id: Optional user ID for direct message
            context: Optional context about what was being processed
            
        Returns:
            True if notification sent successfully
        """
        if not self.telegram_bot:
            logger.warning("Telegram bot not configured, skipping notification")
            return False

        # Build user-friendly error message
        message_parts = [
            "⚠️ <b>Error Occurred</b>",
            "",
            f"<b>Error:</b> {error.message}",
            "",
            f"<b>Category:</b> {error.category.value.replace('_', ' ').title()}",
        ]
        
        if context:
            message_parts.extend([
                "",
                f"<b>Context:</b> {context}"
            ])
        
        # Add retry suggestion
        if error.retry_after:
            message_parts.extend([
                "",
                f"⏳ You can retry in {error.retry_after} seconds."
            ])
        else:
            message_parts.extend([
                "",
                "🔄 Please try again later."
            ])
        
        # Add timestamp
        message_parts.extend([
            "",
            f"<i>Time: {error.timestamp.strftime('%Y-%m-%d %H:%M:%S')} UTC</i>"
        ])
        
        message = "\n".join(message_parts)
        
        try:
            if user_id:
                await self.telegram_bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode="HTML"
                )
            elif self._notification_chat_id:
                await self.telegram_bot.send_message(
                    chat_id=self._notification_chat_id,
                    text=message,
                    parse_mode="HTML"
                )
            return True
            
        except TelegramError as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    async def handle_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        notify: bool = True,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Handle error and optionally notify user
        
        Args:
            error: The exception to handle
            context: Additional context about the error
            notify: Whether to send Telegram notification
            user_id: User ID for direct notification
            
        Returns:
            Error response dictionary
        """
        # Convert to AgenticError if needed
        if not isinstance(error, AgenticError):
            agentic_error = self._classify_error(error)
        else:
            agentic_error = error
        
        # Add context to error
        if context:
            agentic_error.details.update(context)
        
        # Log error
        error_info = {
            **agentic_error.to_dict(),
            "context": context
        }
        self._log_error(error_info)
        
        # Log to file
        logger.error(
            f"Error handled: {agentic_error.message}",
            extra={"error_info": error_info}
        )
        
        # Send notification if requested
        if notify and agentic_error.severity in [
            ErrorSeverity.HIGH, 
            ErrorSeverity.CRITICAL
        ]:
            await self.notify_user(
                error=agentic_error,
                user_id=user_id,
                context=context.get("operation") if context else None
            )
        
        # Return user-friendly response
        return self._build_error_response(agentic_error)

    def _classify_error(self, error: Exception) -> AgenticError:
        """Classify unknown error and wrap in AgenticError"""
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        # Timeout errors
        if any(keyword in error_str for keyword in ["timeout", "timed out", "deadline"]):
            return TimeoutError(message=str(error))
        
        # Database errors
        if any(keyword in error_str for keyword in ["database", "db", "sql", "connection refused"]):
            return DatabaseError(message=str(error))
        
        # Browserless errors
        if any(keyword in error_str for keyword in ["browserless", "chrome", "headless"]):
            return BrowserlessError(message=str(error))
        
        # Default unknown error
        return AgenticError(
            message=f"An unexpected error occurred: {error_type}",
            details={"original_error": str(error)}
        )

    def _log_error(self, error_info: Dict[str, Any]) -> None:
        """Add error to log with size limit"""
        self.error_log.append(error_info)
        if len(self.error_log) > self.max_log_size:
            self.error_log = self.error_log[-self.max_log_size:]

    def _build_error_response(self, error: AgenticError) -> Dict[str, Any]:
        """Build user-friendly error response"""
        return {
            "success": False,
            "error": {
                "message": error.message,
                "category": error.category.value
            },
            "retry_after": error.retry_after,
            "timestamp": error.timestamp.isoformat()
        }

    async def handle_with_fallback(
        self,
        operation: Callable,
        fallback_value: Any,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute operation with error handling and fallback
        
        Args:
            operation: Async function to execute
            fallback_value: Value to return on error
            *args, **kwargs: Arguments for the operation
            
        Returns:
            Operation result or fallback value
        """
        try:
            if callable(operation):
                result = await operation(*args, **kwargs)
            else:
                result = operation
            return result
        except Exception as e:
            error_response = await self.handle_error(e, context={"operation": str(operation)})
            logger.warning(f"Falling back to default value: {e}")
            return fallback_value

    def get_recent_errors(self, limit: int = 10) -> list:
        """Get recent errors from log"""
        return self.error_log[-limit:]

    def get_error_stats(self) -> Dict[str, Any]:
        """Get error statistics"""
        stats = {
            "total_errors": len(self.error_log),
            "by_category": {},
            "by_severity": {}
        }
        
        for error in self.error_log:
            category = error.get("category", "unknown")
            severity = error.get("severity", "medium")
            
            stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
            stats["by_severity"][severity] = stats["by_severity"].get(severity, 0) + 1
        
        return stats


# Global error handler instance
error_handler = ErrorHandler()
