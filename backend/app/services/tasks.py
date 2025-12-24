"""Celery client helpers for enqueuing work from the API layer."""

from celery import Celery

from backend.app.core.config import get_settings

settings = get_settings()

celery = Celery('backend-client', broker=settings.redis_url, backend=settings.redis_url)


def enqueue_fixture_scan(scan_id: str) -> None:
    """Send a task to the worker to process a fixture-based scan run."""
    celery.send_task('worker.app.tasks.scan_tasks.run_fixture_scan', args=[scan_id])
