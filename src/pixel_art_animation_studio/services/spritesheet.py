"""Pack frames into a horizontal or grid spritesheet."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from pixel_art_animation_studio.models.document import AnimationDocument


@dataclass(frozen=True, slots=True)
class SheetLayout:
    columns: int
    rows: int
    frame_width: int
    frame_height: int


def plan_layout(doc: AnimationDocument, columns: int | None = None) -> SheetLayout:
    count = len(doc.frames)
    if count == 0:
        raise ValueError("document has no frames")
    cols = columns or count
    cols = max(1, min(cols, count))
    rows = (count + cols - 1) // cols
    return SheetLayout(cols, rows, doc.width, doc.height)


def pack(doc: AnimationDocument, columns: int | None = None) -> np.ndarray:
    """Return a uint8 RGBA spritesheet of shape (rows*h, cols*w, 4)."""
    layout = plan_layout(doc, columns)
    sheet = np.zeros(
        (layout.rows * layout.frame_height, layout.columns * layout.frame_width, 4),
        dtype=np.uint8,
    )
    for i, frame in enumerate(doc.frames):
        r, c = divmod(i, layout.columns)
        y0 = r * layout.frame_height
        x0 = c * layout.frame_width
        sheet[y0 : y0 + layout.frame_height, x0 : x0 + layout.frame_width] = frame.pixels
    return sheet