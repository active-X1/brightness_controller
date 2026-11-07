import json
import tempfile
import unittest
from pathlib import Path

from brightness_controller.core import Settings, SettingsStore, default_settings_path


class DefaultPathTests(unittest.TestCase):
    home = Path("/home/ada")

    def test_linux_respects_xdg(self):
        path = default_settings_path("linux", {"XDG_CONFIG_HOME": "/xdg"}, self.home)
        self.assertEqual(path, Path("/xdg/brightness-controller/settings.json"))

    def test_linux_falls_back_to_dot_config(self):
        path = default_settings_path("linux", {}, self.home)
        self.assertEqual(path, self.home / ".config" / "brightness-controller" / "settings.json")

    def test_windows_uses_appdata(self):
        path = default_settings_path("win32", {"APPDATA": "C:/Roaming"}, self.home)
        self.assertEqual(path, Path("C:/Roaming/BrightnessController/settings.json"))

    def test_macos(self):
        path = default_settings_path("darwin", {}, self.home)
        self.assertEqual(path.parts[-3:], ("Application Support", "BrightnessController", "settings.json"))


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.path = Path(self._dir.name) / "nested" / "settings.json"
        self.store = SettingsStore(self.path)

    def test_missing_file_gives_defaults(self):
        self.assertEqual(self.store.load(), Settings())

    def test_round_trip_creates_parent_directories(self):
        self.store.save(Settings(theme="dark", startup_prompt_answered=True))
        self.assertEqual(self.store.load(), Settings("dark", True))
        self.assertEqual([p.name for p in self.path.parent.iterdir()], ["settings.json"])

    def test_corrupt_file_gives_defaults(self):
        self.path.parent.mkdir(parents=True)
        for content in ["{not json", "[]", "42", ""]:
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                self.assertEqual(self.store.load(), Settings())

    def test_invalid_values_are_ignored_individually(self):
        self.path.parent.mkdir(parents=True)
        self.path.write_text(
            json.dumps({"theme": "neon", "startup_prompt_answered": "yes", "extra": 1}),
            encoding="utf-8",
        )
        self.assertEqual(self.store.load(), Settings())
        self.path.write_text(json.dumps({"theme": "light"}), encoding="utf-8")
        self.assertEqual(self.store.load(), Settings(theme="light"))


if __name__ == "__main__":
    unittest.main()
