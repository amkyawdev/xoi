"""Log formatters"""

import sys
from typing import Any


class JSONFormatter:
    """Format logs as JSON"""
    
    def format(self, record: dict[str, Any]) -> str:
        """Format log record as JSON"""
        import json
        return json.dumps(record)


class TextFormatter:
    """Format logs as human-readable text"""
    
    def format(self, record: dict[str, Any]) -> str:
        """Format log record as text"""
        timestamp = record.get("timestamp", "")
        level = record.get("level", "INFO").upper()
        logger = record.get("logger", "")
        message = record.get("event", "")
        
        parts = [f"[{timestamp}]", f"[{level}]"]
        if logger:
            parts.append(f"[{logger}]")
        parts.append(message)
        
        return " ".join(parts)


class ColoredFormatter:
    """Format logs with colors"""
    
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[35m",
    }
    RESET = "\033[0m"
    
    def format(self, record: dict[str, Any]) -> str:
        """Format log record with colors"""
        level = record.get("level", "INFO").upper()
        color = self.COLORS.get(level, "")
        
        text = TextFormatter().format(record)
        return f"{color}{text}{self.RESET}"
