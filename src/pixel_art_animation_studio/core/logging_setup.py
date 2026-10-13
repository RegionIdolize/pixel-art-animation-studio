"""Logging configuration shared by CLI and GUI entry points."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from platformdirs import user_log_dir

APP_NAME = "pixel-art-animation-studio"


def configure_logging(level: str | None = None) -> None:
    """Configure root logging once. Safe to call repeatedly."""
    resolved = level or os.environ.get("PAAS_LOG_LEVEL", "INFO")
    log_dir = Path(user_log_dir(APP_NAME))
    log_dir.mkdir(parents=True, exist_ok=True)
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    try:
        handlers.append(logging.FileHandler(log_dir / "studio.log", encoding="utf-8"))
    except OSError:
        pass
    logging.basicConfig(
        level=resolved.upper(),
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        handlers=handlers,
        force=True,
    )