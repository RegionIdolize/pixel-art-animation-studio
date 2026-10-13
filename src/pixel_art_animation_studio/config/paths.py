"""Filesystem path helpers for the studio workspace."""

from __future__ import annotations

from pathlib import Path

SPRITES_DIRNAME = "sprites"
EXPORTS_DIRNAME = "exports"
BACKUPS_DIRNAME = "backups"


def ensure_workspace(root: Path) -> Path:
    """Create the workspace tree if missing and return the root."""
    for name in (SPRITES_DIRNAME, EXPORTS_DIRNAME, BACKUPS_DIRNAME):
        (root / name).mkdir(parents=True, exist_ok=True)
    return root


def sprites_dir(root: Path) -> Path:
    return root / SPRITES_DIRNAME


def exports_dir(root: Path) -> Path:
    return root / EXPORTS_DIRNAME