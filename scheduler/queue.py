"""Task queue"""

import asyncio
from typing import Any, Callable
from collections import deque


class TaskQueue:
    """Simple async task queue"""
    
    def __init__(self, max_size: int = 0):
        self.max_size = max_size
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._workers: list[asyncio.Task] = []
        self._running = False
    
    async def put(self, item: Any) -> None:
        """Add item to queue"""
        await self._queue.put(item)
    
    async def get(self) -> Any:
        """Get item from queue"""
        return await self._queue.get()
    
    def task_done(self) -> None:
        """Mark task as done"""
        self._queue.task_done()
    
    async def join(self) -> None:
        """Wait for all tasks to complete"""
        await self._queue.join()
    
    async def start_workers(self, worker_func: Callable, num_workers: int = 4) -> None:
        """Start worker tasks"""
        self._running = True
        for _ in range(num_workers):
            task = asyncio.create_task(self._worker(worker_func))
            self._workers.append(task)
    
    async def _worker(self, worker_func: Callable) -> None:
        """Worker coroutine"""
        while self._running:
            try:
                item = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                await worker_func(item)
                self._queue.task_done()
            except asyncio.TimeoutError:
                continue
    
    async def stop(self) -> None:
        """Stop all workers"""
        self._running = False
        for task in self._workers:
            task.cancel()
        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()


# Global task queue
task_queue = TaskQueue()
