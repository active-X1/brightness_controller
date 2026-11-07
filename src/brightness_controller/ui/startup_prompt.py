"""One-time dialog asking whether to launch the app when the user signs in."""

from __future__ import annotations

from collections.abc import Callable

import customtkinter as ctk

from brightness_controller import APP_NAME

__all__ = ["StartupPrompt"]


class StartupPrompt(ctk.CTkToplevel):
    """Modal question. ``on_answer(True)`` for yes, ``on_answer(False)`` for no.

    Closing the window with the X button counts as "ask me again next time"
    and does not call ``on_answer``.
    """

    def __init__(self, parent: ctk.CTk, on_answer: Callable[[bool], None]) -> None:
        super().__init__(parent)
        self._on_answer = on_answer
        self.title(APP_NAME)
        self.resizable(False, False)
        self.transient(parent)

        ctk.CTkLabel(self, text="Launch at startup?", font=ctk.CTkFont(size=20, weight="bold")).pack(
            padx=30, pady=(24, 6)
        )
        ctk.CTkLabel(
            self,
            text=(
                f"Would you like {APP_NAME} to start automatically\n"
                "(minimised) when you sign in?\n\n"
                "You can change this any time with the switch\nin the main window."
            ),
            justify="center",
        ).pack(padx=30, pady=(0, 18))

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(0, 22))
        ctk.CTkButton(
            buttons, text="No thanks", width=120, fg_color="gray40", hover_color="gray30",
            command=lambda: self._answer(False),
        ).pack(side="left")
        ctk.CTkButton(
            buttons, text="Yes, launch at startup", width=170, command=lambda: self._answer(True)
        ).pack(side="right")

        # CustomTkinter windows must be visible before they can grab input.
        self.after(150, self._grab)

    def _grab(self) -> None:
        if self.winfo_exists():
            self.grab_set()
            self.focus_set()

    def _answer(self, enabled: bool) -> None:
        self.destroy()
        self._on_answer(enabled)
