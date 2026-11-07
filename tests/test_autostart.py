import tempfile
import unittest
from pathlib import Path

from brightness_controller.core import LinuxAutostart, get_autostart, launch_command
from brightness_controller.core.autostart import _quote_exec


class LaunchCommandTests(unittest.TestCase):
    def test_python_install(self):
        cmd = launch_command(executable="/usr/bin/python3", frozen=False, platform="linux")
        self.assertEqual(cmd, ["/usr/bin/python3", "-m", "brightness_controller", "--minimized"])

    def test_frozen_build_runs_the_executable_directly(self):
        cmd = launch_command(executable="C:/Apps/BrightnessController.exe", frozen=True)
        self.assertEqual(cmd, ["C:/Apps/BrightnessController.exe", "--minimized"])

    def test_windows_prefers_pythonw_when_present(self):
        with tempfile.TemporaryDirectory() as folder:
            python = Path(folder) / "python.exe"
            python.touch()
            (Path(folder) / "pythonw.exe").touch()
            cmd = launch_command(executable=str(python), frozen=False, platform="win32")
        self.assertTrue(cmd[0].endswith("pythonw.exe"))

    def test_windows_keeps_python_exe_without_pythonw(self):
        cmd = launch_command(executable="C:/nowhere/python.exe", frozen=False, platform="win32")
        self.assertEqual(cmd[0], "C:/nowhere/python.exe")


class QuoteTests(unittest.TestCase):
    def test_plain_arguments_are_untouched(self):
        self.assertEqual(_quote_exec("/usr/bin/python3"), "/usr/bin/python3")
        self.assertEqual(_quote_exec("--minimized"), "--minimized")

    def test_spaces_and_specials_are_quoted(self):
        self.assertEqual(_quote_exec("/opt/my app/python"), '"/opt/my app/python"')
        self.assertEqual(_quote_exec("$HOME"), '"\\\\$HOME"')
        self.assertEqual(_quote_exec(""), '""')


class LinuxAutostartTests(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.autostart = LinuxAutostart(Path(self._dir.name) / "autostart")

    def test_enable_disable_cycle(self):
        self.assertFalse(self.autostart.is_enabled())
        self.autostart.enable(["/usr/bin/python3", "-m", "brightness_controller", "--minimized"])
        self.assertTrue(self.autostart.is_enabled())
        self.autostart.disable()
        self.assertFalse(self.autostart.is_enabled())

    def test_disable_when_already_disabled_is_fine(self):
        self.autostart.disable()

    def test_desktop_entry_contents(self):
        self.autostart.enable(["/opt/my app/python", "--minimized"])
        text = self.autostart.path.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("[Desktop Entry]\n"))
        self.assertIn("Type=Application", text)
        self.assertIn('Exec="/opt/my app/python" --minimized', text)
        self.assertIn("Terminal=false", text)

    def test_enable_twice_overwrites(self):
        self.autostart.enable(["/a", "--minimized"])
        self.autostart.enable(["/b", "--minimized"])
        self.assertEqual(self.autostart.path.read_text(encoding="utf-8").count("Exec="), 1)
        self.assertIn("Exec=/b", self.autostart.path.read_text(encoding="utf-8"))


class FactoryTests(unittest.TestCase):
    def test_platform_selection(self):
        self.assertIsInstance(get_autostart("linux"), LinuxAutostart)
        self.assertEqual(type(get_autostart("win32")).__name__, "WindowsAutostart")
        self.assertIsNone(get_autostart("darwin"))


if __name__ == "__main__":
    unittest.main()
