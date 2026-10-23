"""The UI inventory proof covers the controls, handlers, live region and theme tokens."""

import unittest
from pathlib import Path

from tools.ui_inventory import inventory

WEB = Path(__file__).resolve().parent.parent / "web"


class InventoryTest(unittest.TestCase):

    def test_the_inventory_names_the_controls_and_theme_tokens(self):
        entries = inventory(WEB)
        for expected in ("element div#board", "action new", "handler undo",
                         "live-region status", "token --tile-2048-bg"):
            self.assertIn(expected, entries)
        self.assertGreaterEqual(len(entries), 60)

    def test_the_page_and_script_are_part_of_the_surface(self):
        entries = inventory(WEB)
        self.assertIn("element output#score", entries)
        self.assertIn("element output#moves", entries)
        self.assertIn("element button#new-game", entries)
        self.assertIn("handler continue", entries)


if __name__ == "__main__":
    unittest.main()
