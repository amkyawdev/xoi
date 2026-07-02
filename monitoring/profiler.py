"""Performance profiling"""

import time
import functools
from typing import Any, Callable


class Profiler:
    """Profile function performance"""
    
    def __init__(self):
        self.stats: dict[str, list[float]] = {}
    
    def profile(self, func: Callable) -> Callable:
        """Decorator to profile function"""
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = await func(*args, **kwargs)
            duration = time.time() - start
            
            name = f"{func.__module__}.{func.__name__}"
            if name not in self.stats:
                self.stats[name] = []
            self.stats[name].append(duration)
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            
            name = f"{func.__module__}.{func.__name__}"
            if name not in self.stats:
                self.stats[name] = []
            self.stats[name].append(duration)
            
            return result
        
        if asyncio_iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    def get_stats(self) -> dict[str, dict[str, float]]:
        """Get profiling statistics"""
        stats = {}
        for name, durations in self.stats.items():
            if durations:
                stats[name] = {
                    "count": len(durations),
                    "total": sum(durations),
                    "avg": sum(durations) / len(durations),
                    "min": min(durations),
                    "max": max(durations)
                }
        return stats
    
    def reset(self) -> None:
        """Reset statistics"""
        self.stats.clear()


def asyncio_iscoroutinefunction(func: Callable) -> bool:
    """Check if function is async"""
    import asyncio
    return asyncio.iscoroutinefunction(func)


# Global profiler
profiler = Profiler()
