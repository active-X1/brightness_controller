"""Command-line entry point: ``brightness-controller``."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from brightness_controller import APP_NAME, __version__
from brightness_controller.core.autostart import STARTUP_FLAG

__all__ = ["build_parser", "main"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brightness-controller", description=f"{APP_NAME}: control your screen brightness."
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        STARTUP_FLAG,
        dest="minimized",
        action="store_true",
        help="start minimised (used when launched at startup)",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        import tkinter
    except ImportError:
        print(
            "Tkinter is not available in this Python installation.\n"
            "  Debian/Ubuntu: sudo apt install python3-tk\n"
            "  Fedora:        sudo dnf install python3-tkinter"
        )
        return 1
    try:
        from brightness_controller.ui.main_window import MainWindow
    except ImportError as exc:
        print(f"A required package is missing ({exc.name}). Reinstall with: pip install .")
        return 1

    try:
        window = MainWindow(minimized=args.minimized)
    except tkinter.TclError as exc:
        print(f"Could not open a window: {exc}")
        return 1
    window.mainloop()
    return 0
