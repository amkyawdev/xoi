"""CLI utilities"""

import os
from pathlib import Path
from typing import Any, Optional

import yaml
from dotenv import load_dotenv


def get_config_dir() -> Path:
    """Get configuration directory"""
    return Path.home() / ".web-agent-platform"


def ensure_config_dir() -> Path:
    """Ensure configuration directory exists"""
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def load_config(config_path: Optional[Path] = None) -> dict[str, Any]:
    """Load configuration from file"""
    if config_path is None:
        config_path = ensure_config_dir() / "config.yaml"
    
    if config_path.exists():
        with open(config_path) as f:
            return yaml.safe_load(f) or {}
    return {}


def save_config(config: dict[str, Any], config_path: Optional[Path] = None) -> None:
    """Save configuration to file"""
    if config_path is None:
        config_path = ensure_config_dir() / "config.yaml"
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)


def load_env() -> None:
    """Load environment variables from .env file"""
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)


def get_api_url() -> str:
    """Get API URL from environment"""
    return os.getenv("API_URL", "http://localhost:8000")


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as JSON string"""
    import json
    return json.dumps(data, indent=indent, default=str)


def format_markdown(data: Any) -> str:
    """Format data as markdown table"""
    if isinstance(data, list) and data:
        headers = list(data[0].keys())
        rows = [[item.get(h, "") for h in headers] for item in data]
        return _format_table(headers, rows)
    return str(data)


def _format_table(headers: list[str], rows: list[list[Any]]) -> str:
    """Format headers and rows as markdown table"""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    header_line = "| " + " | ".join(h.ljust(w) for h, w in zip(headers, col_widths)) + " |"
    separator = "| " + " | ".join("-" * w for w in col_widths) + " |"
    
    row_lines = []
    for row in rows:
        row_lines.append("| " + " | ".join(str(c).ljust(w) for c, w in zip(row, col_widths)) + " |")
    
    return "\n".join([header_line, separator] + row_lines)
