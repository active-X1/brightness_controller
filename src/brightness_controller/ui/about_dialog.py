"""The About dialog."""

from __future__ import annotations

import webbrowser

import customtkinter as ctk

from brightness_controller import APP_NAME, AUTHOR, REPOSITORY_URL, __version__

__all__ = ["AboutDialog"]


class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent: ctk.CTk) -> None:
        super().__init__(parent)
        self.title(f"About {APP_NAME}")
        self.resizable(False, False)
        self.transient(parent)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(padx=24, pady=(20, 8))

        text = ctk.CTkFrame(body, fg_color="transparent")
        text.pack(side="left", padx=(0, 20))
        ctk.CTkLabel(text, text=APP_NAME, font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(text, text=f"Version {__version__}").pack(anchor="w", pady=4)
        ctk.CTkLabel(
            text,
            text=(
                "A lightweight desktop app\nfor controlling screen brightness.\n\n"
                "Built with Python, CustomTkinter\nand screen-brightness-control."
            ),
            justify="left",
        ).pack(anchor="w")
        ctk.CTkLabel(text, text=f"Developer: {AUTHOR}", font=ctk.CTkFont(size=13, weight="bold")).pack(
            anchor="w", pady=(10, 0)
        )

        ctk.CTkLabel(body, text="\U0001f4a1", text_color="#f5c518", font=ctk.CTkFont(size=72)).pack(
            side="right"
        )

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=24, pady=(0, 18))
        ctk.CTkButton(
            buttons, text="GitHub", width=100, fg_color="gray20", hover_color="gray35",
            command=lambda: webbrowser.open(REPOSITORY_URL),
        ).pack(side="left")
        ctk.CTkButton(buttons, text="Close", width=100, command=self.destroy).pack(side="right")
