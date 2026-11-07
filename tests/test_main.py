import contextlib
import io
import unittest

from brightness_controller import __version__
from brightness_controller.main import build_parser, main


class ParserTests(unittest.TestCase):
    def test_minimized_flag(self):
        self.assertFalse(build_parser().parse_args([]).minimized)
        self.assertTrue(build_parser().parse_args(["--minimized"]).minimized)

    def test_version(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as ctx:
            main(["--version"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn(__version__, out.getvalue())

    def test_unknown_option_exits_with_usage_error(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as ctx:
            main(["--bogus"])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
