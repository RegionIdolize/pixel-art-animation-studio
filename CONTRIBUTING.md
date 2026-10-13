# Contributing to pixel-art-animation-studio

Thanks for wanting to push pixels. This is a plugin-host desktop tool: a small
core (`src/pixel_art_animation_studio/core`) boots a `PluginHost`, loads
extension modules from a registry, and lets plugins register canvas tools,
timeline effects, and exporters.

## Dev setup

```bash
python -m venv .venv
. .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev,export]"
pytest -q
ruff check .
mypy src
```

## Architecture

- `core/` — host lifecycle, frame model, event bus. No UI imports allowed here.
- `handlers/` — Qt-facing controllers that translate UI events into core ops.
- `services/` — stateless-ish helpers (spritesheet packing, onion skin, palette).
- `models/` — dataclasses and typed contracts shared with plugins.
- `utils/` — pure functions, no side effects, unit-tested hard.
- `plugins/` — bundled example extensions loaded through the same registry path
  third-party plugins use.

## Writing a plugin

Subclass `PluginBase`, implement `register(registry)`, and drop the module into
`user_plugins/` or point `PAAS_PLUGIN_PATH` at it. See
`plugins/checkerboard_bg/plugin.py` for the smallest working example. Plugins
must declare `api_version` matching `contracts.API_VERSION` or the loader
quarantines them instead of crashing the host.

## Style

- Ruff + mypy strict. No new dependency without a note in the PR description.
- Keep `core/` importable without Qt — CI runs headless core tests.
- Frame data is `numpy.uint8` RGBA, shape `(height, width, 4)`. Don't mutate
  frames in place across plugin boundaries; copy.

## PRs

One feature per PR. Include a test. If you touch the loader, add a test that
proves a broken plugin is quarantined, not fatal.