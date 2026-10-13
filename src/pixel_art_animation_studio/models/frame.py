"""A single animation frame: RGBA pixel buffer plus timing metadata."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

RGBA = tuple[int, int, int, int]


@dataclass(slots=True)
class Frame:
    """One frame. `pixels` is uint8 RGBA, shape (height, width, 4)."""

    pixels: np.ndarray
    duration_ms: int = 83
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.pixels.dtype != np.uint8:
            raise TypeError(f"frame pixels must be uint8, got {self.pixels.dtype}")
        if self.pixels.ndim != 3 or self.pixels.shape[2] != 4:
            raise ValueError(f"expected (h, w, 4), got {self.pixels.shape}")
        if self.duration_ms <= 0:
            raise ValueError("duration_ms must be positive")

    @property
    def size(self) -> tuple[int, int]:
        h, w, _ = self.pixels.shape
        return (w, h)

    def copy(self) -> "Frame":
        return Frame(self.pixels.copy(), self.duration_ms, self.tags)

    def set_pixel(self, x: int, y: int, rgba: RGBA) -> None:
        self.pixels[y, x] = rgba

    def get_pixel(self, x: int, y: int) -> RGBA:
        r, g, b, a = self.pixels[y, x]
        return (int(r), int(g), int(b), int(a))