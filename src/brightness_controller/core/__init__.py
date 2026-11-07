"""UI-independent logic: brightness control, settings and launch-at-startup."""

from .autostart import Autostart, LinuxAutostart, WindowsAutostart, get_autostart, launch_command
from .brightness import BrightnessError, BrightnessService, clamp_percent
from .settings import THEMES, Settings, SettingsStore, default_settings_path

__all__ = [
    "THEMES",
    "Autostart",
    "BrightnessError",
    "BrightnessService",
    "LinuxAutostart",
    "Settings",
    "SettingsStore",
    "WindowsAutostart",
    "clamp_percent",
    "default_settings_path",
    "get_autostart",
    "launch_command",
]
