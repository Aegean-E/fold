"""The HTTP layer over a real socket: JSON endpoints, static files and hostile input."""

import json
import random
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple

from fold.game import Game
from fold.server import StaticFiles, build_server

START = ((2, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))


class ServerHarness:
    """One server on an ephemeral port, torn down without a lingering thread."""

    def __init__(self, board=START) -> None:
        self.game = Game(random.Random(4), board=board)
        self.server = build_server(self.game, 0)
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       kwargs={"poll_interval": 0.01}, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(2)

    def request(self, path: str, payload: Optional[bytes] = None) -> Tuple[int, bytes]:
        request = urllib.request.Request(self.base + path, data=payload, method="POST" if payload is not None else "GET")
        if payload is not None:
            request.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as error:
            with error:
                return error.code, error.read()


class ServerTest(unittest.TestCase):

    def setUp(self):
        self.harness = ServerHarness()
        self.addCleanup(self.harness.close)

    def test_the_page_and_assets_are_served(self):
        for path, marker in (("/", b'id="board"'), ("/theme.css", b"--paper"),
                             ("/app.css", b".board"), ("/app.js", b"ACTIONS"),
                             ("/favicon.svg", b"<svg")):
            status, body = self.harness.request(path)
            self.assertEqual(200, status, path)
            self.assertIn(marker, body, path)

    def test_security_headers_are_present(self):
        with urllib.request.urlopen(self.harness.base + "/", timeout=5) as response:
            headers = response.headers
        self.assertEqual("nosniff", headers.get("X-Content-Type-Options"))
        self.assertEqual("no-referrer", headers.get("Referrer-Policy"))
        self.assertEqual("same-origin", headers.get("Cross-Origin-Resource-Policy"))
        self.assertIn("default-src 'self'", headers.get("Content-Security-Policy", ""))
        self.assertTrue((headers.get("Server") or "").startswith("fold/"))

    def test_state_returns_the_declared_shape(self):
        status, body = self.harness.request("/api/state")
        state = json.loads(body)
        self.assertEqual(200, status)
        self.assertEqual({"board", "score", "won", "over", "canUndo", "moves", "moved", "gained"},
                         set(state))

    def test_a_move_merges_and_spawns_a_tile(self):
        status, body = self.harness.request("/api/move", b'{"direction":"left"}')
        state = json.loads(body)
        self.assertEqual(200, status)
        self.assertTrue(state["moved"])
        self.assertEqual(4, state["score"])
        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))

    def test_undo_restores_the_previous_board(self):
        before = json.loads(self.harness.request("/api/state")[1])
        self.harness.request("/api/move", b'{"direction":"left"}')
        after = json.loads(self.harness.request("/api/undo", b"{}")[1])
        self.assertEqual(before["board"], after["board"])
        self.assertEqual(before["score"], after["score"])
        self.assertFalse(after["canUndo"])

    def test_a_bad_direction_is_a_400_with_an_error(self):
        status, body = self.harness.request("/api/move", b'{"direction":"diagonal"}')
        self.assertEqual(400, status)
        self.assertIn("direction must be one of", json.loads(body)["error"])

    def test_malformed_json_is_a_400(self):
        status, body = self.harness.request("/api/move", b"{not json")
        self.assertEqual(400, status)
        self.assertIn("not valid JSON", json.loads(body)["error"])

    def test_an_oversized_body_is_a_413(self):
        status, _ = self.harness.request("/api/move", b"{" + b"x" * 5000 + b"}")
        self.assertEqual(413, status)

    def test_an_unknown_route_is_a_json_404(self):
        status, body = self.harness.request("/api/missing")
        self.assertEqual(404, status)
        self.assertEqual("not found", json.loads(body)["error"])

    def test_a_trailing_slash_is_not_the_index(self):
        status, _ = self.harness.request("/missing/")
        self.assertEqual(404, status)


class StaticFilesTest(unittest.TestCase):

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "web").mkdir()
        (self.root / "web" / "index.html").write_text("<p>hi</p>", encoding="utf-8")
        (self.root / "secret.txt").write_text("nope", encoding="utf-8")
        self.files = StaticFiles(self.root / "web")

    def test_root_serves_the_index(self):
        self.assertEqual("index.html", self.files.resolve("/").name)

    def test_paths_outside_the_web_root_are_refused(self):
        self.assertIsNone(self.files.resolve("/../secret.txt"))
        self.assertIsNone(self.files.resolve("/%2e%2e/secret.txt"))
        self.assertIsNone(self.files.resolve("/missing.css"))


if __name__ == "__main__":
    unittest.main()
