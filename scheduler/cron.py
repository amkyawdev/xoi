"""Cron scheduler"""

from typing import Callable, Any
from datetime import datetime
import asyncio


class CronJob:
    """Cron job definition"""
    
    def __init__(self, name: str, func: Callable, cron_expr: str, **kwargs: Any):
        self.name = name
        self.func = func
        self.cron_expr = cron_expr
        self.kwargs = kwargs
        self._running = False
    
    async def run(self) -> Any:
        """Run the job"""
        result = self.func(**self.kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result


class CronScheduler:
    """Simple cron scheduler"""
    
    def __init__(self):
        self.jobs: list[CronJob] = []
        self._running = False
        self._task: asyncio.Task | None = None
    
    def add_job(self, name: str, func: Callable, cron_expr: str, **kwargs: Any) -> CronJob:
        """Add a cron job"""
        job = CronJob(name, func, cron_expr, **kwargs)
        self.jobs.append(job)
        return job
    
    def remove_job(self, name: str) -> None:
        """Remove a cron job"""
        self.jobs = [j for j in self.jobs if j.name != name]
    
    async def start(self) -> None:
        """Start the scheduler"""
        self._running = True
        self._task = asyncio.create_task(self._run())
    
    async def stop(self) -> None:
        """Stop the scheduler"""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
    
    async def _run(self) -> None:
        """Run scheduler loop"""
        while self._running:
            now = datetime.now()
            
            for job in self.jobs:
                if self._should_run(job, now):
                    asyncio.create_task(job.run())
            
            await asyncio.sleep(60)  # Check every minute
    
    def _should_run(self, job: CronJob, now: datetime) -> bool:
        """Check if job should run now"""
        # Simple implementation - would parse cron expression properly
        return True  # Placeholder
