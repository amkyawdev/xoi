"""Distributed tracing"""

import time
from contextlib import contextmanager
from typing import Any, Generator


class Tracer:
    """Simple tracing implementation"""
    
    def __init__(self, service_name: str = "web-agent-platform"):
        self.service_name = service_name
        self.spans: list[dict[str, Any]] = []
    
    @contextmanager
    def span(self, name: str, attributes: dict[str, Any] | None = None) -> Generator[dict[str, Any], None, None]:
        """Create a new span"""
        span = {
            "name": name,
            "service": self.service_name,
            "start_time": time.time(),
            "attributes": attributes or {},
            "events": []
        }
        
        try:
            yield span
        finally:
            span["end_time"] = time.time()
            span["duration"] = span["end_time"] - span["start_time"]
            self.spans.append(span)
    
    def add_event(self, span: dict[str, Any], name: str, attributes: dict[str, Any] | None = None) -> None:
        """Add event to span"""
        span["events"].append({
            "name": name,
            "timestamp": time.time(),
            "attributes": attributes or {}
        })
    
    def get_traces(self) -> list[dict[str, Any]]:
        """Get all recorded spans"""
        return self.spans


# Global tracer
tracer = Tracer()
