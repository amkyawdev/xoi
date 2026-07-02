"""Logging configuration"""

import sys
from typing import Any


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": "logs/app.log"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"]
    },
    "loggers": {
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "fastapi": {
            "level": "INFO",
            "handlers": ["console"]
        }
    }
}


def setup_logging(level: str = "INFO") -> None:
    """Setup logging configuration"""
    import logging.config
    LOGGING_CONFIG["root"]["level"] = level
    logging.config.dictConfig(LOGGING_CONFIG)
