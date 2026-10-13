"""Color math helpers for pixel operations."""

from __future__ import annotations

RGBA = tuple[int, int, int, int]


def clamp_channel(value: int) -> int:
    return max(0, min(255, value))


def hex_to_rgba