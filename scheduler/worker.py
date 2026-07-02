"""Celery worker"""

from celery import Celery


celery_app = Celery(
    "web_agent_platform",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task(name="crawl_url")
def crawl_url(url: str, depth: int = 2) -> dict:
    """Crawl URL task"""
    return {"url": url, "depth": depth, "status": "completed"}


@celery_app.task(name="process_content")
def process_content(content: str, operation: str) -> dict:
    """Process content task"""
    return {"operation": operation, "status": "completed"}


@celery_app.task(name="send_notification")
def send_notification(message: str, recipient: str) -> dict:
    """Send notification task"""
    return {"recipient": recipient, "status": "sent"}
