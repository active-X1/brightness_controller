# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-10-24

A restructure of the original single-file app into an installable package.

### Added
- **Startup prompt:** on first launch the app asks whether it should launch at
  startup. The choice is remembered and can be changed at any time with the new
  "Launch at startup" switch.
- Launch-at-startup support for Windows (per-user registry entry) and Linux
  (XDG autostart entry), started minimised with `--minimized`.
- The theme choice (System / Light / Dark) is now remembered between runs.
- `brightness-controller` command and `python -m brightness_controller`.
- Unit tests, `pyproject.toml`, Ruff/mypy configuration and GitHub Actions CI.
- MIT license, README, contributing guide.

### Changed
- Code split into `core` (brightness, settings, autostart) and `ui` packages.
- Brightness is applied at most ~16 times per second while dragging the slider,
  so the window no longer lags on slow hardware. The final value always applies.
- The About dialog's GitHub button now opens the repository.

### Fixed
- The app crashed on startup when no controllable display was found. It now
  opens with the slider disabled and explains what is wrong.
- Errors while changing brightness are shown in the window instead of being
  raised from inside the slider callback.

### Removed
- The About dialog's "Portfolio" button, which had no link attached.
