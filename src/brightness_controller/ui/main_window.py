"""The main window."""

from __future__ import annotations

import customtkinter as ctk

from brightness_controller import APP_NAME
from brightness_controller.core import (
    Autostart,
    BrightnessError,
    BrightnessService,
    SettingsStore,
    clamp_percent,
    get_autostart,
    launch_command,
)

from .about_dialog import AboutDialog
from .startup_prompt import StartupPrompt

__all__ = ["MainWindow"]

#: The slider fires on every pixel of a drag; hardware calls can be slow, so
#: brightness is applied at most once per interval (the last value always wins).
APPLY_INTERVAL_MS = 60
PROMPT_DELAY_MS = 500
THEME_LABELS = ("System", "Light", "Dark")


class MainWindow(ctk.CTk):
    def __init__(
        self,
        *,
        service: BrightnessService | None = None,
        store: SettingsStore | None = None,
        autostart: Autostart | None = None,
        minimized: bool = False,
    ) -> None:
        store = store if store is not None else SettingsStore()
        settings = store.load()
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(settings.theme)
        super().__init__()

        self.store = store
        self.settings = settings
        self.autostart = autostart if autostart is not None else get_autostart()
        self._pending_level: int | None = None
        self._apply_job: str | None = None

        self.title(APP_NAME)
        self.geometry("540x290")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.close)

        initial: int | None = None
        error = ""
        try:
            self.service = service if service is not None else BrightnessService()
            initial = self.service.get()
        except BrightnessError as exc:
            self.service = service  # may be None when the backend is missing
            error = str(exc)

        self._build_widgets(initial, error)

        if minimized:
            self.after(100, self.iconify)
        elif self.autostart is not None and not self.settings.startup_prompt_answered:
            self.after(PROMPT_DELAY_MS, self._ask_about_startup)

    # ------------------------------------------------------------------ layout

    def _build_widgets(self, initial: int | None, error: str) -> None:
        ctk.CTkLabel(self, text="Brightness Control", font=ctk.CTkFont(size=30, weight="bold")).pack(
            pady=(22, 14)
        )

        card = ctk.CTkFrame(self, height=56)
        card.pack(padx=30, fill="x")
        card.pack_propagate(False)
        self.level_label = ctk.CTkLabel(
            card, text="Level --" if initial is None else f"Level {initial}%",
            font=ctk.CTkFont(size=20, weight="bold"), width=110,
        )
        self.level_label.pack(side="left", padx=(16, 8))
        self.slider = ctk.CTkSlider(
            card, from_=0, to=100, number_of_steps=100, command=self._on_slider
        )
        self.slider.pack(side="right", expand=True, fill="x", padx=(0, 16))
        self.slider.set(50 if initial is None else initial)
        if initial is None:
            self.slider.configure(state="disabled")

        self.status_label = ctk.CTkLabel(
            self, text=error, text_color=("#b42318", "#f97066"), wraplength=480, height=36
        )
        self.status_label.pack(padx=30, pady=(6, 0))

        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(side="bottom", fill="x", padx=30, pady=(0, 18))
        self.theme_button = ctk.CTkSegmentedButton(
            bar, values=list(THEME_LABELS), command=self._on_theme
        )
        self.theme_button.pack(side="left")
        self.theme_button.set(self.settings.theme.capitalize())

        ctk.CTkButton(bar, text="\u2139 About", width=80, command=self.show_about).pack(side="right")

        self.startup_switch: ctk.CTkSwitch | None = None
        if self.autostart is not None:
            self.startup_switch = ctk.CTkSwitch(
                bar, text="Launch at startup", command=self._on_startup_switch
            )
            self.startup_switch.pack(side="right", padx=(0, 18))
            if self._startup_enabled():
                self.startup_switch.select()

    # ---------------------------------------------------------------- brightness

    def _on_slider(self, value: float) -> None:
        level = clamp_percent(value)
        self.level_label.configure(text=f"Level {level}%")
        self._pending_level = level
        if self._apply_job is None:
            self._apply_job = self.after(APPLY_INTERVAL_MS, self._apply_pending)

    def _apply_pending(self) -> None:
        self._apply_job = None
        level, self._pending_level = self._pending_level, None
        if level is None or self.service is None:
            return
        try:
            self.service.set(level)
        except BrightnessError as exc:
            self._set_status(str(exc))
        else:
            self._set_status("")

    # -------------------------------------------------------------------- theme

    def _on_theme(self, label: str) -> None:
        self.settings.theme = label.lower()
        ctk.set_appearance_mode(self.settings.theme)
        self._save_settings()

    # ------------------------------------------------------------------ startup

    def _startup_enabled(self) -> bool:
        try:
            return self.autostart is not None and self.autostart.is_enabled()
        except OSError:
            return False

    def _on_startup_switch(self) -> None:
        assert self.startup_switch is not None
        wanted = bool(self.startup_switch.get())
        if not self._set_startup(wanted):
            # Revert the switch to what is actually registered.
            if wanted:
                self.startup_switch.deselect()
            else:
                self.startup_switch.select()

    def _set_startup(self, enabled: bool) -> bool:
        """Register or unregister launch-at-startup. Returns ``True`` on success."""
        if self.autostart is None:
            return False
        try:
            if enabled:
                self.autostart.enable(launch_command())
            else:
                self.autostart.disable()
        except OSError as exc:
            self._set_status(f"Could not change the startup setting: {exc}")
            return False
        self._set_status("")
        return True

    def _ask_about_startup(self) -> None:
        StartupPrompt(self, self._on_startup_answer)

    def _on_startup_answer(self, enabled: bool) -> None:
        self.settings.startup_prompt_answered = True
        self._save_settings()
        if enabled and self._set_startup(True) and self.startup_switch is not None:
            self.startup_switch.select()

    # ------------------------------------------------------------------- helpers

    def show_about(self) -> None:
        AboutDialog(self)

    def _set_status(self, text: str) -> None:
        self.status_label.configure(text=text)

    def _save_settings(self) -> None:
        try:
            self.store.save(self.settings)
        except OSError as exc:
            self._set_status(f"Could not save settings: {exc}")

    def close(self) -> None:
        """Apply any brightness change still waiting, then exit."""
        if self._apply_job is not None:
            self.after_cancel(self._apply_job)
            self._apply_job = None
            self._apply_pending()
        self.destroy()
