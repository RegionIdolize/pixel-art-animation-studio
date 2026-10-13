"""Shared plugin contracts. Bump API_VERSION on any breaking change."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from pixel_art_animation_studio.core.registry import PluginRegistry
from pixel_art_animation_studio.models.document import AnimationDocument
from pixel_art_animation_studio.models.frame import Frame

API_VERSION = "0.6"


@runtime_checkable
class PluginBase(Protocol):
    """Every plugin implements this. `api_version` must match API_VERSION."""

    name: str
    api_version: str

    def register(self, registry: PluginRegistry) -> None: ...

    def dispose(self) -> None: ...


@runtime_checkable
class CanvasTool(Protocol):
    """A tool the user can select to paint on the active frame."""

    tool_id: str
    label: str

    def begin(self, frame: Frame, x: int, y: int, color: tuple[int, int, int, int]) -> None: ...

    def drag(self, frame: Frame, x: int, y: int) -> None: ...

    def end(self, frame: Frame) -> None: ...


@runtime_checkable
class TimelineEffect(Protocol):
    """Transforms the document when applied (e.g. shift, tween, reverse)."""

    effect_id: str
    label: str

    def apply(self, document: AnimationDocument) -> None: ...