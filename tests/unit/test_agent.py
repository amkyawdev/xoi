"""Unit tests for agent module"""

import pytest

from agent.planner import Planner, Task
from agent.executor import Executor
from agent.memory import Memory


@pytest.fixture
def planner():
    return Planner()


@pytest.fixture
def memory():
    return Memory()


def test_create_task():
    """Test task creation"""
    task = Task(id="1", description="Test task")
    assert task.id == "1"
    assert task.description == "Test task"
    assert task.status == "pending"


@pytest.mark.asyncio
async def test_planner_create_plan(planner):
    """Test plan creation"""
    tasks = await planner.create_plan("Test goal")
    assert len(tasks) == 1
    assert tasks[0].description == "Test goal"


@pytest.mark.asyncio
async def test_planner_add_task(planner):
    """Test adding tasks"""
    task = await planner.add_task("New task")
    assert task.id == "1"
    assert task.description == "New task"


@pytest.mark.asyncio
async def test_memory_add_recall(memory):
    """Test memory operations"""
    memory.add("Test content")
    results = memory.recall("Test")
    assert len(results) == 1
    assert results[0]["content"] == "Test content"


def test_memory_get_recent(memory):
    """Test getting recent memories"""
    memory.add("Content 1")
    memory.add("Content 2")
    recent = memory.get_recent(2)
    assert len(recent) == 2
