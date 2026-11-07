"""Brightness reading and writing, behind a small error-friendly wrapper."""

from __future__ import annotations

import importlib
from typing import Any

__all__ = ["BrightnessError", "BrightnessService", "clamp_percent"]

_HINT = (
    "Your display may not support software brightness control "
    "(external monitors usually need DDC/CI enabled)."
)


class BrightnessError(RuntimeError):
    """Raised when brightness cannot be read or changed."""


def clamp_percent(value: float) -> int:
    """Round ``value`` to a whole number between 0 and 100."""
    return max(0, min(100, int(round(value))))


class BrightnessService:
    """Reads and sets the brightness of the connected display(s) as a percentage.

    ``backend`` is anything with ``get_brightness()`` and ``set_brightness(value)``
    (the ``screen_brightness_control`` module by default). Injecting a fake keeps
    the rest of the app testable without real hardware.
    """

    def __init__(self, backend: Any | None = None) -> None:
        self._backend = backend if backend is not None else _load_backend()

    def get(self) -> int:
        """Current brightness (0-100) of the first display."""
        try:
            levels = self._backend.get_brightness()
        except Exception as exc:  # the backend raises many platform-specific types
            raise BrightnessError(f"Could not read brightness: {exc}") from exc
        values = [v for v in levels if isinstance(v, (int, float)) and not isinstance(v, bool)]
        if not values:
            raise BrightnessError(f"No controllable display was found. {_HINT}")
        return clamp_percent(values[0])

    def set(self, percent: float) -> int:
        """Set the brightness of all displays. Returns the value that was applied."""
        level = clamp_percent(percent)
        try:
            self._backend.set_brightness(level)
        except Exception as exc:
            raise BrightnessError(f"Could not set brightness: {exc}") from exc
        return level


def _load_backend() -> Any:
    try:
        return importlib.import_module("screen_brightness_control")
    except ImportError as exc:
        raise BrightnessError(
            "The 'screen-brightness-control' package is not installed."
        ) from exc
