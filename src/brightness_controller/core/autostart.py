"""Launch-at-startup support for Windows and Linux.

* Windows: a value under ``HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run``.
* Linux: a ``.desktop`` file in ``~/.config/autostart``.

Both are per-user and need no administrator rights.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

__all__ = [
    "Autostart",
    "LinuxAutostart",
    "WindowsAutostart",
    "get_autostart",
    "launch_command",
]

APP_ID = "brightness-controller"
DISPLAY_NAME = "Brightness Controller"
STARTUP_FLAG = "--minimized"


class Autostart(Protocol):
    """Registers the app to run when the user signs in."""

    def is_enabled(self) -> bool: ...

    def enable(self, command: Sequence[str] | None = None) -> None: ...

    def disable(self) -> None: ...


def launch_command(
    *,
    executable: str | None = None,
    frozen: bool | None = None,
    platform: str | None = None,
) -> list[str]:
    """The command that starts the app minimised at sign-in."""
    executable = sys.executable if executable is None else executable
    frozen = bool(getattr(sys, "frozen", False)) if frozen is None else frozen
    platform = sys.platform if platform is None else platform
    if frozen:  # a PyInstaller build: the executable is the app
        return [executable, STARTUP_FLAG]
    if platform == "win32" and executable.lower().endswith("python.exe"):
        windowless = executable[: -len("python.exe")] + "pythonw.exe"  # no console window
        if Path(windowless).exists():
            executable = windowless
    return [executable, "-m", "brightness_controller", STARTUP_FLAG]


class LinuxAutostart:
    """XDG autostart entry (works on GNOME, KDE, Xfce, Cinnamon, ...)."""

    def __init__(self, directory: Path | None = None) -> None:
        if directory is None:
            config = os.environ.get("XDG_CONFIG_HOME") or str(Path.home() / ".config")
            directory = Path(config) / "autostart"
        self.path = directory / f"{APP_ID}.desktop"

    def is_enabled(self) -> bool:
        return self.path.is_file()

    def enable(self, command: Sequence[str] | None = None) -> None:
        command = launch_command() if command is None else command
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            "[Desktop Entry]\n"
            "Type=Application\n"
            f"Name={DISPLAY_NAME}\n"
            "Comment=Control screen brightness\n"
            f"Exec={' '.join(_quote_exec(arg) for arg in command)}\n"
            "Terminal=false\n"
            "X-GNOME-Autostart-enabled=true\n",
            encoding="utf-8",
        )

    def disable(self) -> None:
        self.path.unlink(missing_ok=True)


def _quote_exec(argument: str) -> str:
    """Quote one argument for the ``Exec=`` key of a desktop entry."""
    if argument and not any(ch in argument for ch in ' \t\n"\'\\><~|&;$*?#()`'):
        return argument
    escaped = (
        argument.replace("\\", "\\\\\\\\")
        .replace('"', '\\\\"')
        .replace("`", "\\\\`")
        .replace("$", "\\\\$")
    )
    return f'"{escaped}"'


class WindowsAutostart:  # pragma: no cover - needs the Windows registry
    """``HKCU\\...\\Run`` registry value."""

    KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    VALUE = "BrightnessController"

    def is_enabled(self) -> bool:
        import winreg

        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.KEY) as key:
                winreg.QueryValueEx(key, self.VALUE)
        except FileNotFoundError:
            return False
        return True

    def enable(self, command: Sequence[str] | None = None) -> None:
        import winreg

        command = launch_command() if command is None else command
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.KEY) as key:
            winreg.SetValueEx(key, self.VALUE, 0, winreg.REG_SZ, subprocess.list2cmdline(command))

    def disable(self) -> None:
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, self.KEY, 0, winreg.KEY_SET_VALUE
            ) as key:
                winreg.DeleteValue(key, self.VALUE)
        except FileNotFoundError:
            pass


def get_autostart(platform: str | None = None) -> Autostart | None:
    """The autostart handler for this OS, or ``None`` if it isn't supported."""
    platform = sys.platform if platform is None else platform
    if platform == "win32":
        return WindowsAutostart()
    if platform.startswith("linux"):
        return LinuxAutostart()
    return None
