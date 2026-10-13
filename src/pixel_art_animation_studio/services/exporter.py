"""Export services: PNG sequence, spritesheet PNG, and optional GIF."""

from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

from pixel_art_animation_studio.models.document import AnimationDocument
from pixel_art_animation_studio.services.spritesheet import pack

log = logging.getLogger(__name__)


def export_png_sequence(doc: AnimationDocument, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, frame in enumerate(doc.frames):
        path = out_dir / f"frame_{i:04d}.png"
        Image.fromarray(frame.pixels, mode="RGBA").save(path)
        written.append(path)
    return written


def export_spritesheet(doc: AnimationDocument, path: Path, columns: int | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet = pack(doc, columns)
    Image.fromarray(sheet, mode="RGBA").save(path)
    return path


def export_gif(doc: AnimationDocument, path: Path) -> Path:
    """Requires the `export` extra. Falls back to a clear error otherwise."""
    try:
        import imageio.v3 as iio
    except ImportError as exc:  # pragma: no cover - depends on extras
        raise RuntimeError("install pixel-art-animation-studio[export] for GIF export") from exc
    path.parent.mkdir(parents=True, exist_ok=True)
    frames = [f.pixels for f in doc.frames]
    duration = max(1, round(1000 / doc.fps))
    iio.imwrite(path, frames, duration=duration, loop=0)
    return path