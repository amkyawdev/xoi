"""Alerting system"""

from typing import Any
from datetime import datetime


class Alert:
    """Alert model"""
    
    def __init__(self, severity: str, message: str, **kwargs: Any):
        self.severity = severity  # critical, error, warning, info
        self.message = message
        self.timestamp = datetime.utcnow()
        self.data = kwargs
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return {
            "severity": self.severity,
            "message": self.message,
            "timestamp": self.timestamp.isoformat(),
            **self.data
        }


class AlertManager:
    """Manage and route alerts"""
    
    def __init__(self):
        self.handlers: dict[str, list[Callable]] = {
            "critical": [],
            "error": [],
            "warning": [],
            "info": []
        }
        self.alerts: list[Alert] = []
    
    def register_handler(self, severity: str, handler: Callable[[Alert], None]) -> None:
        """Register alert handler"""
        if severity in self.handlers:
            self.handlers[severity].append(handler)
    
    async def send(self, alert: Alert) -> None:
        """Send alert to handlers"""
        self.alerts.append(alert)
        
        for handler in self.handlers.get(alert.severity, []):
            try:
                result = handler(alert)
                if asyncio_iscoroutinefunction(handler):
                    await result
            except Exception:
                pass
    
    def get_recent(self, limit: int = 100) -> list[Alert]:
        """Get recent alerts"""
        return self.alerts[-limit:]


def asyncio_iscoroutinefunction(func: Any) -> bool:
    """Check if function is async"""
    import asyncio
    return asyncio.iscoroutinefunction(func)


# Global alert manager
alerts = AlertManager()
