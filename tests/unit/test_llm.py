"""Unit tests for LLM module"""

import pytest

from llm.models import Message, ModelConfig
from llm.router import LLM Router


def test_message_creation():
    """Test message creation"""
    msg = Message(role="user", content="Hello")
    assert msg.role == "user"
    assert msg.content == "Hello"


def test_model_config():
    """Test model config"""
    config = ModelConfig(
        name="gpt-4",
        provider="openai",
        context_length=8192
    )
    assert config.name == "gpt-4"
    assert config.context_length == 8192


def test_router_select_model():
    """Test model selection"""
    router = LLM Router()
    model = router.select_model()
    assert model is not None


def test_router_filter_by_capability():
    """Test filtering by capability"""
    router = LLM Router()
    model = router.select_model(capabilities=["vision"])
    assert "vision" in router.get_model(model).capabilities
