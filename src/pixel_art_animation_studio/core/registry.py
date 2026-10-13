"""Plugin registry: where extensions declare canvas tools, effects, exporters."""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import Protocol, runtime_checkable

log = logging.getLogger(__name__)


@runtime_checkable
class Disposable(Protocol):
    def dispose(self) -> None: ...


class PluginRegistry:
    """Holds registered extension points keyed by stable string ids."""

    _SLOTS = ("canvas_tools", "timeline_effects", "exporters", "palette_sources")

    def __init__(self) -> None:
        self._slots: dict[str, dict[str, object]] = {slot: {} for slot in self._SLOTS}

    def register(self, slot: str, key: str, value: object) -> None:
        if slot not in self._slots:
            raise KeyError(f"unknown registry slot: {slot!r}")
        if key in self._slots[slot]:
            log.warning("overriding %s/%s", slot, key)
        self._slots[slot][key] = value

    def get(self, slot: str, key: str) -> object | None:
        return self._slots.get(slot, {}).get(key)

    def items(self, slot: str) -> Iterable[tuple[str, object]]:
        return tuple(self._slots.get(slot, {}).items())

    def dispose_all(self) -> None:
        for slot in self._SLOTS:
            for key, value in self._slots[slot].items():
                if isinstance(value, Disposable):
                    try:
                        value.dispose()
                    except Exception:  # noqa: BLE001
                        log.exception("dispose failed for %s/%s", slot, key)
            self._slots[slot].clear()