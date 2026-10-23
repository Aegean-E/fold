"""
The local HTTP layer: static files from `web/` and four JSON endpoints.

The handler only translates requests into `Game` calls. The game rules, scoring and undo
trail live in `fold.game`, so they are tested without a socket. Every game mutation runs
under one lock because the server is threaded; a request may render while another moves.

PRINCIPLE-009, PRINCIPLE-010, PRINCIPLE-011, PRINCIPLE-013.
"""

import json
import threading
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import unquote, urlparse

from fold.game import Game

MAX_BODY_BYTES = 4096
READ_TIMEOUT_SECONDS = 10
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".svg": "image/svg+xml",
}
WEB_ROOT = Path(__file__).resolve().parent.parent / "web"
POST_ROUTES = ("/api/new", "/api/move", "/api/undo")


@dataclass(frozen=True)
class StaticFiles:
    """Resolves a URL path to a file inside one directory, and never outside it."""

    root: Path

    def resolve(self, url_path: str) -> Optional[Path]:
        """The file a decoded URL path names, or None when it escapes or does not exist."""
        relative = unquote(url_path).lstrip("/") or "index.html"
        candidate = (self.root / relative).resolve()
        try:
            candidate.relative_to(self.root.resolve())
        except ValueError:
            return None
        return candidate if candidate.is_file() else None


class FoldHandler(BaseHTTPRequestHandler):
    """Translates requests into `Game` reads and mutations."""

    protocol_version = "HTTP/1.1"
    server_version = "fold/1.0"
    sys_version = ""
    timeout = READ_TIMEOUT_SECONDS
    disable_nagle_algorithm = True
    wbufsize = 64 * 1024
    game: Game
    lock: threading.Lock
    files: StaticFiles

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler contract
        route = unquote(urlparse(self.path).path)
        if route == "/api/state":
            with self.lock:
                payload = self.game.state()
            self._json(200, payload)
            return
        target = self.files.resolve(route)
        if target is None:
            self._json(404, {"error": "not found", "path": route})
            return
        body = target.read_bytes()
        self._respond(200, CONTENT_TYPES.get(target.suffix, "application/octet-stream"),
                      body, cache=route != "/" and not route.endswith(".html"))

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler contract
        route = unquote(urlparse(self.path).path)
        if route not in POST_ROUTES:
            self._json(404, {"error": "not found", "path": route})
            return
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self._json(400, {"error": "Content-Length must be an integer"})
            return
        if length < 0:
            self._json(400, {"error": "Content-Length must not be negative"})
            return
        if length > MAX_BODY_BYTES:
            self.close_connection = True
            self._json(413, {"error": f"body over {MAX_BODY_BYTES} bytes"})
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = self._payload(raw)
            with self.lock:
                result = self._act(route, payload)
        except ValueError as error:
            self._json(400, {"error": str(error)})
            return
        self._json(200, result)

    def _payload(self, raw: bytes) -> Dict[str, object]:
        """Decode one JSON object; anything else is a 400, never a traceback."""
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError) as error:
            raise ValueError(f"body is not valid JSON: {error}") from error
        if not isinstance(payload, dict):
            raise ValueError("body must be a JSON object")
        return payload

    def _act(self, route: str, payload: Dict[str, object]) -> Dict[str, object]:
        """Apply one named endpoint to the game and return its read model."""
        if route == "/api/new":
            return self.game.reset()
        if route == "/api/undo":
            return self.game.undo()
        direction = payload.get("direction")
        if not isinstance(direction, str):
            raise ValueError("body needs a string 'direction'")
        return self.game.move(direction)

    def _json(self, status: int, payload: Dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self._respond(status, "application/json; charset=utf-8", body, cache=False)

    def _respond(self, status: int, content_type: str, body: bytes, cache: bool) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "max-age=60" if cache else "no-store")
        self.end_headers()
        self.wfile.write(body)
        self.wfile.flush()

    def end_headers(self) -> None:
        """Attach the security policy to every response, including stdlib errors."""
        self.send_header("Content-Security-Policy",
                         "default-src 'self'; img-src 'self' data:; style-src 'self'; "
                         "script-src 'self'; connect-src 'self'; base-uri 'none'; "
                         "form-action 'self'; frame-ancestors 'none'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        super().end_headers()

    def log_message(self, format: str, *args) -> None:
        """Silent by default; `fold.cli` prints the one line a user needs."""


class FoldHTTPServer(ThreadingHTTPServer):
    """A local thread-per-request server whose threads do not outlive the process."""

    daemon_threads = True


def build_server(game: Game, port: int, web: Path = WEB_ROOT,
                 host: str = "127.0.0.1") -> FoldHTTPServer:
    """An HTTP server bound to `host:port`, serving `web` and one in-memory game."""
    handler = type("BoundFoldHandler", (FoldHandler,), {
        "game": game,
        "lock": threading.Lock(),
        "files": StaticFiles(web),
    })
    return FoldHTTPServer((host, port), handler)
