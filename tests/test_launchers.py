"""One-click launch files: present, CRLF-safe on Windows and pointing at run.py."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BATCH = ROOT / "play.bat"
SHELL = ROOT / "play.sh"
COMMAND = ROOT / "play.command"
START_BATCH = ROOT / "start.bat"
START_SHELL = ROOT / "start.sh"
START_COMMAND = ROOT / "start.command"


class LauncherTest(unittest.TestCase):

    def test_every_launcher_exists(self):
        for path in (BATCH, SHELL, COMMAND, START_BATCH, START_SHELL, START_COMMAND):
            self.assertTrue(path.is_file(), path.name)

    def test_batch_files_have_crlf_line_endings(self):
        for path in (BATCH, START_BATCH):
            data = path.read_bytes()
            self.assertEqual(0, data.replace(b"\r\n", b"").count(b"\n"),
                             f"{path.name} must use CRLF so cmd.exe parses it reliably")

    def test_launchers_start_the_game_and_aliases_delegate(self):
        self.assertIn("run.py --open", BATCH.read_text(encoding="utf-8"))
        self.assertIn("run.py --open", SHELL.read_text(encoding="utf-8"))
        self.assertIn("sh ./play.sh", COMMAND.read_text(encoding="utf-8"))
        self.assertIn("play.bat", START_BATCH.read_text(encoding="utf-8"))
        self.assertIn("play.sh", START_SHELL.read_text(encoding="utf-8"))
        self.assertIn("play.sh", START_COMMAND.read_text(encoding="utf-8"))

    def test_a_batch_failure_stays_visible(self):
        self.assertIn("pause", BATCH.read_text(encoding="utf-8").lower())

    def test_gitattributes_pins_launcher_line_endings(self):
        attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("*.bat text eol=crlf", attributes)
        self.assertIn("*.sh text eol=lf", attributes)


if __name__ == "__main__":
    unittest.main()
