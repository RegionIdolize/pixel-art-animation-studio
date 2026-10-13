# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.6.x   | yes       |
| < 0.6   | no        |

## Reporting a vulnerability

Email `security@pixel-art-animation-studio.dev` with a description, a minimal
repro, and the affected version. We aim to acknowledge within 72 hours.

## Threat model

pixel-art-animation-studio loads third-party plugin modules from disk. That is
by design and is the primary attack surface.

- The plugin loader **does not sandbox** plugin code. A plugin runs with the
  same privileges as the host process, including filesystem and network access.
  Only load plugins you trust.
- `PluginLoader` validates `api_version` and required attributes before
  `import`, but a malicious module can execute arbitrary code at import time.
  There is no signature verification in 0.6.x.
- Autosave writes to `platformdirs.user_data_dir` by default. Keep the
  workspace directory out of synced/shared folders if your frames are sensitive.
- Exporters shell out to `imageio-ffmpeg` only when the `export` extra is
  installed; the ffmpeg binary path is resolved from the environment.

We will not treat "a plugin you installed ran code" as a vulnerability. We
will treat loader path traversal, workspace symlink escapes, and ffmpeg
argument injection as vulnerabilities — please report those.