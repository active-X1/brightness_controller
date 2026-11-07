import unittest

from brightness_controller.core import BrightnessError, BrightnessService, clamp_percent


class FakeBackend:
    def __init__(self, levels=None, error=None):
        self.levels = [40] if levels is None else levels
        self.error = error
        self.calls = []

    def get_brightness(self):
        if self.error:
            raise self.error
        return self.levels

    def set_brightness(self, value):
        if self.error:
            raise self.error
        self.calls.append(value)


class ClampTests(unittest.TestCase):
    def test_clamp(self):
        for value, expected in [(-5, 0), (0, 0), (49.6, 50), (100, 100), (250, 100)]:
            with self.subTest(value=value):
                self.assertEqual(clamp_percent(value), expected)


class ServiceTests(unittest.TestCase):
    def test_get_returns_first_display(self):
        self.assertEqual(BrightnessService(FakeBackend([72, 10])).get(), 72)

    def test_get_ignores_unusable_values(self):
        self.assertEqual(BrightnessService(FakeBackend([None, 55])).get(), 55)

    def test_get_with_no_display(self):
        with self.assertRaisesRegex(BrightnessError, "No controllable display"):
            BrightnessService(FakeBackend([])).get()

    def test_get_wraps_backend_errors(self):
        with self.assertRaisesRegex(BrightnessError, "Could not read"):
            BrightnessService(FakeBackend(error=OSError("nope"))).get()

    def test_set_clamps_and_applies(self):
        backend = FakeBackend()
        service = BrightnessService(backend)
        self.assertEqual(service.set(150), 100)
        self.assertEqual(service.set(-3), 0)
        self.assertEqual(service.set(41.4), 41)
        self.assertEqual(backend.calls, [100, 0, 41])

    def test_set_wraps_backend_errors(self):
        with self.assertRaisesRegex(BrightnessError, "Could not set"):
            BrightnessService(FakeBackend(error=RuntimeError("x"))).set(10)


if __name__ == "__main__":
    unittest.main()
