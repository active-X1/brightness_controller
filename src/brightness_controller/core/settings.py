"""Persistent user settings stored as a small JSON file."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path

__all__ = ["THEMES", "Settings", "SettingsStore", "default_settings_path"]

THEMES = ("system", "light", "dark")


@dataclass
class Settings:
    """User preferences."""

    theme: str = "system"
    #: Whether the one-time "launch at startup?" question has been answered.
    startup_prompt_answered: bool = False


def default_settings_path(
    platform: str | None = None,
    env: Mapping[str, str] | None = None,
    home: Path | None = None,
) -> Path:
    """Where settings live for the current OS (arguments exist for testing)."""
    platform = sys.platform if platform is None else platform
    env = os.environ if env is None else env
    home = Path.home() if home is None else home
    if platform == "win32":
        base = Path(env.get("APPDATA") or home / "AppData" / "Roaming")
        return base / "BrightnessController" / "settings.json"
    if platform == "darwin":
        return home / "Library" / "Application Support" / "BrightnessController" / "settings.json"
    base = Path(env.get("XDG_CONFIG_HOME") or home / ".config")
    return base / "brightness-controller" / "settings.json"


class SettingsStore:
    """Loads and saves :class:`Settings`. Never raises on a missing or corrupt file."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path if path is not None else default_settings_path()

    def load(self) -> Settings:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return Settings()
        if not isinstance(data, dict):
            return Settings()
        settings = Settings()
        if data.get("theme") in THEMES:
            settings.theme = data["theme"]
        if isinstance(data.get("startup_prompt_answered"), bool):
            settings.startup_prompt_answered = data["startup_prompt_answered"]
        return settings

    def save(self, settings: Settings) -> None:
        """Write atomically so a crash can't leave a half-written file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(asdict(settings), handle, indent=2)
            os.replace(tmp_name, self.path)
        except BaseException:
            Path(tmp_name).unlink(missing_ok=True)
            raise
