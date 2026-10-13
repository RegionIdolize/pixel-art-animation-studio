"""Minimal synchronous event bus used between core, handlers, and plugins."""

from __future__ import annotations

import logging
from collections import defaultdict
from collections.abc import Callable
from typing import Any

log = logging.getLogger(__name__)

Listener = Callable[[dict[str, Any]], None]


class EventBus:
    """Publish/subscribe over string topics. Handlers run in publish order."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Listener]] = defaultdict(list)

    def subscribe(self, topic: str, listener: Listener) -> Callable[[], None]:
        self._listeners[topic].append(listener)

        def _unsubscribe() -> None:
            try:
                self._listeners[topic].remove(listener)
            except ValueError:
                pass

        return _unsubscribe

    def publish(self, topic: str, payload: dict[str, Any] | None = None) -> None:
        payload = payload or {}
        for listener in tuple(self._listeners.get(topic, ())):
            try:
                listener(payload)
            except Exception:  # noqa: BLE001 - a bad listener must not kill the bus
                log.exception("listener failed on topic %s", topic)