"""Command-line parsing: local defaults, an optional seed and a validated port."""

import argparse
import contextlib
import io
import unittest

from fold.cli import parse_args, port_number


class CliTest(unittest.TestCase):

    def test_defaults_keep_the_game_local(self):
        args = parse_args([])
        self.assertEqual(8766, args.port)
        self.assertEqual("127.0.0.1", args.host)
        self.assertIsNone(args.seed)
        self.assertFalse(args.open)

    def test_a_seed_and_open_are_opt_in(self):
        args = parse_args(["--seed", "7", "--open"])
        self.assertEqual(7, args.seed)
        self.assertTrue(args.open)

    def test_a_port_outside_the_valid_range_is_refused(self):
        for value in ("0", "65536", "http"):
            with self.assertRaises(argparse.ArgumentTypeError):
                port_number(value)

    def test_a_valid_port_is_an_integer(self):
        self.assertEqual(8080, port_number("8080"))

    def test_a_bad_flag_exits_two_with_a_triad(self):
        stderr = io.StringIO()
        with self.assertRaises(SystemExit) as caught:
            with contextlib.redirect_stderr(stderr):
                parse_args(["--port", "0"])
        self.assertEqual(2, caught.exception.code)
        self.assertIn("Why:", stderr.getvalue())
        self.assertIn("Fix:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
