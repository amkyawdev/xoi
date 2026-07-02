"""Workflow orchestration"""

from typing import Any

from agent.planner import Planner
from agent.executor import Executor
from agent.reasoning import ReasoningEngine


class Workflow:
    """Orchestrates the agent workflow"""
    
    def __init__(self):
        self.planner = Planner()
        self.executor = Executor(self.planner)
        self.reasoning = ReasoningEngine()
    
    async def run(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the complete workflow"""
        # Reasoning phase
        reasoning_result = await self.reasoning.think(goal, context)
        
        # Planning phase
        tasks = await self.planner.create_plan(goal)
        
        # Execution phase
        results = await self.executor.execute_all()
        
        return {
            "goal": goal,
            "reasoning": reasoning_result,
            "tasks": [t.model_dump() for t in tasks],
            "results": results
        }
    
    async def run_step(self, step: str) -> Any:
        """Run a single step"""
        return await self.executor.execute_until_complete(step)
    
    def get_status(self) -> dict[str, Any]:
        """Get current workflow status"""
        return {
            "pending_tasks": sum(1 for t in self.planner.tasks.values() if t.status == "pending"),
            "completed_tasks": sum(1 for t in self.planner.tasks.values() if t.status == "completed"),
            "failed_tasks": sum(1 for t in self.planner.tasks.values() if t.status == "failed"),
        }
