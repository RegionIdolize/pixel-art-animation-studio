"""Qt application shell: main window, canvas view, timeline dock."""

from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from pixel_art_animation_studio.core.host import StudioHost
from pixel_art_animation_studio.handlers.main_window import MainWindow

log = logging.getLogger(__name__)


def run_app(host: StudioHost, argv: list[str]) -> int:
    """Start the Qt event loop. Returns the process exit code."""
    app = QApplication.instance() or QApplication(argv)
    app.setApplicationName("pixel-art-animation-studio")
    window = MainWindow(host)
    window.show()
    return app.exec()