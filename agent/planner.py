"""Task planner for agent"""

from typing import Any
from pydantic import BaseModel


class Task(BaseModel):
    """Task model"""
    id: str
    description: str
    status: str = "pending"
    dependencies: list[str] = []
    result: Any = None


class Planner:
    """Plans and decomposes tasks into executable steps"""
    
    def __init__(self):
        self.tasks: dict[str, Task] = {}
    
    async def create_plan(self, goal: str) -> list[Task]:
        """Create a plan for the given goal"""
        task = Task(id="1", description=goal)
        self.tasks[task.id] = task
        return [task]
    
    async def add_task(self, description: str, dependencies: list[str] | None = None) -> Task:
        """Add a new task to the plan"""
        task_id = str(len(self.tasks) + 1)
        task = Task(
            id=task_id,
            description=description,
            dependencies=dependencies or []
        )
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Task | None:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_ready_tasks(self) -> list[Task]:
        """Get tasks that are ready to execute"""
        ready = []
        for task in self.tasks.values():
            if task.status != "pending":
                continue
            deps_complete = all(
                self.tasks.get(dep_id, Task(id="", description="", status="completed")).status == "completed"
                for dep_id in task.dependencies
            )
            if deps_complete:
                ready.append(task)
        return ready
    
    async def complete_task(self, task_id: str, result: Any) -> None:
        """Mark task as completed"""
        if task_id in self.tasks:
            self.tasks[task_id].status = "completed"
            self.tasks[task_id].result = result
