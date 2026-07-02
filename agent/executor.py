"""Task executor for agent"""

from typing import Any, Callable, Awaitable

from agent.planner import Planner, Task


class Executor:
    """Executes tasks based on plan"""
    
    def __init__(self, planner: Planner):
        self.planner = planner
        self.tools: dict[str, Callable[..., Awaitable[Any]]] = {}
    
    def register_tool(self, name: str, func: Callable[..., Awaitable[Any]]) -> None:
        """Register a tool function"""
        self.tools[name] = func
    
    async def execute_task(self, task: Task) -> Any:
        """Execute a single task"""
        task.status = "running"
        
        try:
            # Placeholder - actual execution logic
            result = {"status": "completed", "task_id": task.id}
            await self.planner.complete_task(task.id, result)
            return result
        except Exception as e:
            task.status = "failed"
            raise
    
    async def execute_all(self) -> dict[str, Any]:
        """Execute all tasks in the plan"""
        results = {}
        
        while True:
            ready_tasks = self.planner.get_ready_tasks()
            if not ready_tasks:
                break
            
            for task in ready_tasks:
                result = await self.execute_task(task)
                results[task.id] = result
        
        return results
    
    async def execute_until_complete(self, goal: str) -> dict[str, Any]:
        """Create plan and execute until complete"""
        await self.planner.create_plan(goal)
        return await self.execute_all()
