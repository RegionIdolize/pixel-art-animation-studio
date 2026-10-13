"""Palette model with nearest-color lookup for indexed drawing."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

RGBA = tuple[int, int, int, int]


@dataclass(slots=True)
class Palette:
    """Ordered palette. Colors are RGBA tuples; alpha is usually 255."""

    name: str
    colors: list[RGBA] = field(default_factory=list)

    def add(self, rgba: RGBA) -> int:
        self.colors.append(rgba)
        return len(self.colors) - 1

    def nearest(self, rgba: RGBA) -> RGBA:
        """Return the palette color closest to `rgba` in RGB space."""
        if not self.colors:
            return rgba
        target = np.array(rgba[:3], dtype=np.int32)
        stack = np.array([c[:3] for c in self.colors], dtype=np.int32)
        deltas = stack - target
        idx = int(np.argmin((deltas * deltas).sum(axis=1)))
        return self.colors[idx]

    @classmethod
    def default_16(cls) -> "Palette":
        return cls(
            name="default-16",
            colors=[
                (0, 0, 0, 255),
                (29, 43, 83, 255),
                (126, 37, 83, 255),
                (0, 135, 81, 255),
                (171, 82, 54, 255),
                (95, 87, 79, 255),
                (194, 195, 199, 255),
                (255, 241, 232, 255),
                (255, 0, 77, 255),
                (255, 163, 0, 255),
                (255, 236, 39, 255),
                (0, 228, 54, 255),
                (41, 173, 255, 255),
                (131, 118, 156, 255),
                (255, 119, 168, 255),
                (255, 204, 170, 255),
            ],
        )