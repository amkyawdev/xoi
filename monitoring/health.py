"""Health checks"""

from typing import Any


class HealthChecker:
    """Health check aggregator"""
    
    def __init__(self):
        self.checks: dict[str, Callable[[], dict[str, Any]]] = {}
    
    def register_check(self, name: str, check: Callable[[], dict[str, Any]]) -> None:
        """Register a health check"""
        self.checks[name] = check
    
    async def check_all(self) -> dict[str, Any]:
        """Run all health checks"""
        results = {}
        
        for name, check in self.checks.items():
            try:
                result = check()
                if asyncio_iscoroutinefunction(check):
                    result = await result
                results[name] = {"status": "healthy", **result}
            except Exception as e:
                results[name] = {"status": "unhealthy", "error": str(e)}
        
        overall_status = "healthy" if all(r.get("status") == "healthy" for r in results.values()) else "unhealthy"
        
        return {
            "status": overall_status,
            "checks": results
        }


def asyncio_iscoroutinefunction(func: Any) -> bool:
    """Check if function is async"""
    import asyncio
    return asyncio.iscoroutinefunction(func)


# Global health checker
health_checker = HealthChecker()
