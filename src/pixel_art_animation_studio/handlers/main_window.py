"""MainWindow wires the host document to the canvas and timeline widgets."""

from __future__ import annotations

from PySide6.QtWidgets import QDockWidget, QMainWindow

from pixel_art_animation_studio.core.host import StudioHost
from pixel_art_animation_studio.handlers.canvas_view import CanvasView
from pixel_art_animation_studio.handlers.timeline_panel import TimelinePanel


class MainWindow(QMainWindow):
    def __init__(self, host: StudioHost) -> None:
        super().__init__()
        self.host = host
        self.setWindowTitle("pixel-art-animation-studio")
        self.resize(1180, 720)

        self.canvas = CanvasView(host)
        self.setCentralWidget(self.canvas)

        dock = QDockWidget("Timeline", self)
        dock.setWidget(TimelinePanel(host))
        self.addDockWidget(self._bottom_area(), dock)

        host.events.subscribe("document.changed", self._on_document_changed)

    @staticmethod
    def _bottom_area():
        from PySide6.QtCore import Qt

        return Qt.DockWidgetArea.BottomDockWidgetArea

    def _on_document_changed(self, _payload: dict) -> None:
        self.canvas.update()