"""Timeline dock: frame strip, add/remove, and playback controls."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pixel_art_animation_studio.core.host import StudioHost


class TimelinePanel(QWidget):
    def __init__(self, host: StudioHost) -> None:
        super().__init__()
        self.host = host
        self._list = QListWidget()
        self._add = QPushButton("Add frame")
        self._remove = QPushButton("Remove frame")

        self._add.clicked.connect(self._on_add)
        self._remove.clicked.connect(self._on_remove)

        controls = QHBoxLayout()
        controls.addWidget(self._add)
        controls.addWidget(self._remove)

        layout = QVBoxLayout(self)
        layout.addWidget(self._list)
        layout.addLayout(controls)

        self.refresh()
        host.events.subscribe("document.changed", lambda _p: self.refresh())

    def refresh(self) -> None:
        self._list.clear()
        for i, frame in enumerate(self.host.document.frames):
            self._list.addItem(f"Frame {i + 1}  ({frame.duration_ms} ms)")

    def _on_add(self) -> None:
        self.host.document.add_frame()
        self.host.events.publish("document.changed", {})

    def _on_remove(self) -> None:
        row = self._list.currentRow()
        if row < 0:
            return
        try:
            self.host.document.remove_frame(row)
        except ValueError:
            return
        self.host.events.publish("document.changed", {})