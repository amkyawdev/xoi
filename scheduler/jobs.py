"""Scheduled jobs"""

from typing import Any, Callable
from datetime import datetime


class Job:
    """Scheduled job"""
    
    def __init__(self, name: str, func: Callable, schedule: str, **kwargs: Any):
        self.name = name
        self.func = func
        self.schedule = schedule
        self.kwargs = kwargs
        self.last_run: datetime | None = None
        self.next_run: datetime | None = None
        self.enabled = True
    
    async def run(self) -> Any:
        """Execute job"""
        self.last_run = datetime.utcnow()
        result = self.func(**self.kwargs)
        
        if hasattr(result, "__await__"):
            return await result
        return result


class JobRegistry:
    """Register and manage jobs"""
    
    def __init__(self):
        self.jobs: dict[str, Job] = {}
    
    def register(self, name: str, schedule: str, **kwargs: Any) -> Callable:
        """Decorator to register job"""
        def decorator(func: Callable) -> Callable:
            self.jobs[name] = Job(name, func, schedule, **kwargs)
            return func
        return decorator
    
    def get_job(self, name: str) -> Job | None:
        """Get job by name"""
        return self.jobs.get(name)
    
    def list_jobs(self) -> list[Job]:
        """List all jobs"""
        return list(self.jobs.values())
    
    def enable(self, name: str) -> None:
        """Enable job"""
        if job := self.jobs.get(name):
            job.enabled = True
    
    def disable(self, name: str) -> None:
        """Disable job"""
        if job := self.jobs.get(name):
            job.enabled = False


# Global job registry
jobs = JobRegistry()


# Example jobs
@jobs.register("cleanup_cache", "0 2 * * *")  # Daily at 2 AM
async def cleanup_cache():
    """Clean up expired cache entries"""
    from cache.memory_cache import cache
    removed = cache.cleanup()
    print(f"Cleaned up {removed} cache entries")
    return removed
