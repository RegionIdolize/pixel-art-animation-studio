"""Canvas widget: renders the active frame scaled with nearest-neighbor."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QWidget

from pixel_art_animation_studio.core.host import StudioHost
from pixel_art_animation_studio.models.frame import Frame


class CanvasView(QWidget):
    """Displays the current frame. Painting tools attach via drag handlers."""

    def __init__(self, host: StudioHost) -> None:
        super().__init__()
        self.host = host
        self.active_index = 0
        self._zoom = 6
        self.setMinimumSize(320, 240)
        self.setMouseTracking(True)

    def active_frame(self) -> Frame:
        return self.host.document.frames[self.active_index]

    def to_qimage(self, frame: Frame) -> QImage:
        h, w, _ = frame.pixels.shape
        buf = frame.pixels.tobytes()
        image = QImage(buf, w, h, w * 4, QImage.Format.Format_RGBA8888)
        return image.copy()

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt override
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        image = self.to_qimage(self.active_frame())
        target = self.rect()
        scaled = image.scaled(
            target.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation,
        )
        painter.drawImage(target.center() - scaled.rect().center(), scaled)
        painter.end()