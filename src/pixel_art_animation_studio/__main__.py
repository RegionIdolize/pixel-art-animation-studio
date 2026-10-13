"""Entry point: boot the plugin host and hand control to the Qt shell."""

from __future__ import annotations

import sys

from pixel_art_animation_studio.core.host import StudioHost
from pixel_art_animation_studio.core.logging_setup import configure_logging


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv if argv is None else argv)
    configure_logging()
    host = StudioHost.from_environment()
    try:
        host.start()
        from pixel_art_animation_studio.handlers.app_window import run_app

        return run_app(host, argv)
    finally:
        host.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())