"""Onion-skin compositing for the canvas preview."""

from __future__ import annotations

import numpy as np

from pixel_art_animation_studio.models.frame import Frame

MAX_GHOSTS = 3


def composite(frame: Frame, neighbors: list[tuple[Frame, float]]) -> np.ndarray:
    """Blend `frame` over tinted ghost frames. Weights in [0, 1]."""
    out = frame.pixels.astype(np.float32)
    for ghost, weight in neighbors[:MAX_GHOSTS]:
        if weight <= 0.0:
            continue
        ghost_rgb = ghost.pixels[..., :3].astype(np.float32)
        ghost_rgb *= np.array([1.0, 0.55, 0.55], dtype=np.float32)
        alpha = (ghost.pixels[..., 3:4].astype(np.float32) / 255.0) * weight
        out[..., :3] = out[..., :3] * (1 - alpha) + ghost_rgb * alpha
    return np.clip(out, 0, 255).astype(np.uint8)


def ghost_neighbors(frames: list[Frame], index: int, radius: int = 1) -> list[tuple[Frame, float]]:
    """Frames before `index`, weighted by distance. Tinting happens in composite."""
    out: list[tuple[Frame, float]] = []
    for offset in range(1, radius + 1):
        j = index - offset
        if 0 <= j < len(frames):
            out.append((frames[j], 0.5 / offset))
    return out