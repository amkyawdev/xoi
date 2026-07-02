"""Agent tools registry"""

from typing import Any, Callable, Awaitable
from functools import wraps


ToolFunc = Callable[..., Awaitable[Any]]


class ToolRegistry:
    """Registry for agent tools"""
    
    def __init__(self):
        self._tools: dict[str, dict[str, Any]] = {}
    
    def register(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any] | None = None
    ) -> Callable[[ToolFunc], ToolFunc]:
        """Decorator to register a tool"""
        def decorator(func: ToolFunc) -> ToolFunc:
            @wraps(func)
            async def wrapper(*args, **kwargs) -> Any:
                return await func(*args, **kwargs)
            
            self._tools[name] = {
                "function": func,
                "description": description,
                "parameters": parameters or {}
            }
            return wrapper
        return decorator
    
    def get_tool(self, name: str) -> dict[str, Any] | None:
        """Get tool by name"""
        return self._tools.get(name)
    
    def list_tools(self) -> list[dict[str, Any]]:
        """List all registered tools"""
        return [
            {"name": name, **tool}
            for name, tool in self._tools.items()
        ]
    
    async def call_tool(self, name: str, **kwargs) -> Any:
        """Call a tool by name"""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        return await tool["function"](**kwargs)


# Global registry
registry = ToolRegistry()


# Built-in tools
@registry.register(
    name="search",
    description="Search the web",
    parameters={"query": {"type": "string"}}
)
async def search_tool(query: str) -> list[dict[str, str]]:
    """Search tool implementation"""
    return [{"title": "Result 1", "url": "https://example.com", "snippet": "..."}]


@registry.register(
    name="scrape",
    description="Scrape a webpage",
    parameters={"url": {"type": "string"}}
)
async def scrape_tool(url: str) -> str:
    """Scrape tool implementation"""
    return f"Content from {url}"


@registry.register(
    name="crawl",
    description="Crawl a website",
    parameters={"url": {"type": "string"}, "depth": {"type": "integer"}}
)
async def crawl_tool(url: str, depth: int = 2) -> list[str]:
    """Crawl tool implementation"""
    return [url]
