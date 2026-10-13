"""AnimationDocument: ordered frames, fps, and mutation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from pixel_art_animation_studio.models.frame import Frame


@dataclass
class AnimationDocument:
    """The editable animation. Not thread-safe; mutate from the UI thread."""

    width: int
    height: int
    fps: int = 12
    frames: list[Frame] = field(default_factory=list)
    dirty: bool = False

    @classmethod
    def empty(cls, width: int, height: int, fps: int = 12) -> "AnimationDocument":
        doc = cls(width=width, height=height, fps=fps)
        doc.frames.append(doc.blank_frame())
        return doc

    def blank_frame(self) -> Frame:
        pixels = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        return Frame(pixels, duration_ms=max(1, round(1000 / self.fps)))

    def add_frame(self, index: int | None = None) -> int:
        frame = self.blank_frame()
        if index is None:
            self.frames.append(frame)
            self.dirty = True
            return len(self.frames) - 1
        self.frames.insert(index, frame)
        self.dirty = True
        return index

    def remove_frame(self, index: int) -> None:
        if len(self.frames) <= 1:
            raise ValueError("cannot remove the last remaining frame")
        del self.frames[index]
        self.dirty = True

    def duration_ms(self) -> int:
        return sum(f.duration_ms for f in self.frames)