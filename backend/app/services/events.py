"""Event publishing helpers for websocket fan-out via Redis."""

import json
from typing import Any, Dict

import redis

from backend.app.core.config import get_settings

settings = get_settings()


def _publish(channel: str, payload: Dict[str, Any]) -> None:
    client = redis.from_url(settings.redis_url)
    client.publish(channel, json.dumps(payload))


def publish_scan_event(payload: Dict[str, Any]) -> None:
    _publish('scans', payload)


def publish_alert_event(payload: Dict[str, Any]) -> None:
    _publish('alerts', payload)
