"""Typed settings loaded from TOML, environment, and defaults."""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

APP_NAME = "pixel-art-animation-studio"
DEFAULT_CANVAS = (64, 64)
DEFAULT_FPS = 12


@dataclass(slots=True)
class StudioSettings:
    """Resolved runtime settings. Immutable after `load`."""

    workspace_dir: Path
    plugin_paths: tuple[Path, ...] = ()
    canvas_width: int = DEFAULT_CANVAS[0]
    canvas_height: int = DEFAULT_CANVAS[1]
    fps: int = DEFAULT_FPS
    autosave_seconds: int = 90
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, config_file: Path | None = None) -> "StudioSettings":
        config_file = config_file or Path(user_config_dir(APP_NAME)) / "studio.toml"
        raw: dict = {}
        if config_file.is_file():
            with config_file.open("rb") as fh:
                raw = tomllib.load(fh)

        workspace = Path(
            os.environ.get(
                "PAAS_WORKSPACE",
                raw.get("workspace_dir", user_data_dir(APP_NAME)),
            )
        )
        plugin_env = os.environ.get("PAAS_PLUGIN_PATH", "")
        plugin_paths = tuple(
            Path(p).expanduser()
            for p in ([*raw.get("plugin_paths", []), *plugin_env.split(os.pathsep)])
            if p
        )
        return cls(
            workspace_dir=workspace,
            plugin_paths=plugin_paths,
            canvas_width=int(raw.get("canvas_width", DEFAULT_CANVAS[0])),
            canvas_height=int(raw.get("canvas_height", DEFAULT_CANVAS[1])),
            fps=int(raw.get("fps", DEFAULT_FPS)),
            autosave_seconds=int(raw.get("autosave_seconds", 90)),
        )