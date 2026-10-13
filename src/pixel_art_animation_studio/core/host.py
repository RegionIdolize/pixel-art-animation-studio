"""StudioHost: owns the frame document, plugin registry, and event bus."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from pixel_art_animation_studio.config.paths import ensure_workspace
from pixel_art_animation_studio.config.settings import StudioSettings
from pixel_art_animation_studio.core.events import EventBus
from pixel_art_animation_studio.core.registry import PluginRegistry
from pixel_art_animation_studio.models.document import AnimationDocument

log = logging.getLogger(__name__)


@dataclass
class StudioHost:
    """Lifecycle owner for the running studio instance."""

    settings: StudioSettings
    document: AnimationDocument = field(init=False)
    events: EventBus = field(default_factory=EventBus)
    registry: PluginRegistry = field(default_factory=PluginRegistry)
    _started: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        self.document = AnimationDocument.empty(
            self.settings.canvas_width, self.settings.canvas_height
        )

    @classmethod
    def from_environment(cls) -> "StudioHost":
        return cls(settings=StudioSettings.load())

    def start(self) -> None:
        if self._started:
            return
        ensure_workspace(self.settings.workspace_dir)
        from pixel_art_animation_studio.plugins.loader import PluginLoader

        loader = PluginLoader(self.registry, self.settings.plugin_paths)
        report = loader.load_all()
        log.info(
            "host started: %d plugins loaded, %d quarantined",
            len(report.loaded),
            len(report.quarantined),
        )
        self._started = True
        self.events.publish("host.started", {"loaded": report.loaded})

    def shutdown(self) -> None:
        if not self._started:
            return
        self.events.publish("host.shutting_down", {})
        self.registry.dispose_all()
        self._started = False

    @property
    def running(self) -> bool:
        return self._started