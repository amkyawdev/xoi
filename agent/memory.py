"""Agent memory management"""

from typing import Any
from datetime import datetime


class Memory:
    """Stores agent conversation and execution history"""
    
    def __init__(self):
        self.short_term: list[dict[str, Any]] = []
        self.long_term: dict[str, list[dict[str, Any]]] = {}
    
    def add(self, content: str, memory_type: str = "short") -> None:
        """Add to memory"""
        entry = {
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "type": memory_type
        }
        
        if memory_type == "short":
            self.short_term.append(entry)
        else:
            key = f"{datetime.utcnow().date()}"
            if key not in self.long_term:
                self.long_term[key] = []
            self.long_term[key].append(entry)
    
    def recall(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        """Recall memories matching query"""
        results = []
        for entry in self.short_term:
            if query.lower() in entry["content"].lower():
                results.append(entry)
        return results[:limit]
    
    def clear_short_term(self) -> None:
        """Clear short-term memory"""
        self.short_term.clear()
    
    def get_recent(self, limit: int = 10) -> list[dict[str, Any]]:
        """Get recent memories"""
        return self.short_term[-limit:]
    
    def get_all(self) -> dict[str, Any]:
        """Get all memories"""
        return {
            "short_term": self.short_term,
            "long_term": self.long_term
        }
