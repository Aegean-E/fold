#!/usr/bin/env python3
"""
Fold's dogfood runner: play it the way a user does, then attack the surface.

The golden path starts a real server on a free port, loads the page, starts a game,
makes a real move, undoes it and reads the state back. The chaos track sends malformed
JSON, bad directions, oversized bodies, concurrent reads, traversal attempts and unknown
routes. Every process runs inside a context manager that kills its whole tree, the run
uses one temporary sandbox and the tracked tree is fingerprinted before and after.

Usage: python tools/dogfood.py   (exit 0 pass, 1 fail, 2 cannot run)

PRINCIPLE-015.
"""

import contextlib
import hashlib
import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / ".aikit" / "dogfood_last_run.log"
MAX_REPORT_LINES = 15
START_TIMEOUT = 20.0
REQUEST_TIMEOUT = 5.0
SUBPROCESS_TIMEOUT = 30
STATE_FIELDS = ("board", "score", "won", "over", "canUndo", "moves", "moved", "gained")
CONTROLS = (b'id="board"', b'id="new-game"', b'id="undo"', b'id="status"',
            b'data-action="new"', b'data-action="undo"')
DIRECTIONS = ("left", "up", "right", "down")


class Report:
    """Collects step outcomes: the console sees a summary, the log sees everything."""

    def __init__(self) -> None:
        self.lines: List[str] = []
        self.failures: List[str] = []

    def step(self, ok: bool, label: str, detail: str = "") -> bool:
        """Record one step's outcome and hand back whether it passed."""
        mark = "PASS" if ok else "FAIL"
        self.lines.append(f"[{mark}] {label}" + (f" :: {detail}" if detail else ""))
        if not ok:
            self.failures.append(f"{label}: {detail}" if detail else label)
        return ok


def terminate_process_tree(process: subprocess.Popen) -> None:
    """Kill a process and everything it started, on Windows and POSIX alike."""
    if process.poll() is not None:
        return
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)],
                           capture_output=True, timeout=SUBPROCESS_TIMEOUT)
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
    except (OSError, subprocess.SubprocessError):
        process.kill()
    with contextlib.suppress(subprocess.TimeoutExpired):
        process.wait(timeout=10)


@contextlib.contextmanager
def supervised(command: List[str], log):
    """Run a command with stdin closed, killing its whole tree on the way out."""
    if os.name == "nt":
        creation = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
    else:
        creation = {"start_new_session": True}
    options = dict(stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                   cwd=str(ROOT), **creation)
    process = subprocess.Popen(command, **options)  # hygiene: allow RAII teardown
    try:
        yield process
    finally:
        terminate_process_tree(process)


def free_port() -> int:
    """A port the operating system says is free right now."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def fingerprint() -> str:
    """A digest of every tracked file, so a run that dirties the repository fails."""
    listing = subprocess.run(["git", "ls-files", "-z"], cwd=str(ROOT), capture_output=True,
                             timeout=SUBPROCESS_TIMEOUT)
    digest = hashlib.sha256()
    for name in sorted(part for part in listing.stdout.split(b"\0") if part):
        digest.update(name)
        path = ROOT / name.decode("utf-8")
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def get(base: str, path: str) -> Tuple[int, bytes, float]:
    """One GET, with the milliseconds it took."""
    started = time.monotonic()
    try:
        with urllib.request.urlopen(base + path, timeout=REQUEST_TIMEOUT) as response:
            body = response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        with error:
            return error.code, error.read(), (time.monotonic() - started) * 1000.0
    return status, body, (time.monotonic() - started) * 1000.0


def post(base: str, path: str, payload: object, raw: Optional[bytes] = None) -> Tuple[int, bytes]:
    """One POST; an HTTP error is an answer here, not an exception."""
    data = raw if raw is not None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(base + path, data=data, method="POST",
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        with error:
            return error.code, error.read()


def wait_until_serving(base: str) -> bool:
    """True once the server answers, False if it never does within the start timeout."""
    deadline = time.monotonic() + START_TIMEOUT
    while time.monotonic() < deadline:
        try:
            get(base, "/api/state")
            return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.05)
    return False


def golden_path(base: str, report: Report) -> None:
    """Load the page, make a move, undo it and read the state back."""
    status, page, _ = get(base, "/")
    report.step(status == 200 and all(control in page for control in CONTROLS),
                "page serves every control the script renders into",
                f"HTTP {status}, {len(page)} bytes")

    code, body, elapsed = get(base, "/api/state")
    first = json.loads(body)
    report.step(code == 200 and all(field in first for field in STATE_FIELDS),
                "GET /api/state answers the declared schema", f"HTTP {code}")
    report.step(elapsed < 500.0, "state answers inside its 500ms budget", f"{elapsed:.0f}ms")
    report.step(sum(1 for row in first["board"] for value in row if value) == 2,
                "a fresh game starts with two tiles")

    moved = None
    for direction in DIRECTIONS:
        code, body = post(base, "/api/move", {"direction": direction})
        candidate = json.loads(body)
        if code == 200 and candidate["moved"]:
            moved = candidate
            break
    report.step(moved is not None, "at least one direction moves the opening board")

    if moved is not None:
        count = sum(1 for row in moved["board"] for value in row if value)
        report.step(count >= 2 and moved["canUndo"] is True,
                    "a real move spawns a tile and leaves an undo",
                    f"{count} tiles, score {moved['score']}")
        code, body = post(base, "/api/undo", {})
        restored = json.loads(body)
        report.step(code == 200 and restored["board"] == first["board"],
                    "undo restores the opening board", f"HTTP {code}")


def chaos(base: str, report: Report) -> None:
    """Hostile input: malformed JSON, bad directions, a flood and traversal."""
    code, body = post(base, "/api/move", None, raw=b"{not json at all")
    report.step(code == 400 and b"error" in body, "malformed JSON answers 400", f"HTTP {code}")

    code, body = post(base, "/api/move", {"direction": "diagonal"})
    report.step(code == 400 and b"direction must be one of" in body,
                "a bad direction answers 400", f"HTTP {code}")

    code, _ = post(base, "/api/move", None, raw=b"{" + b"x" * 8192 + b"}")
    report.step(code == 413, "an oversized body answers 413", f"HTTP {code}")

    code, _ = post(base, "/api/move", [1, 2, 3])
    report.step(code == 400, "a JSON array body answers 400", f"HTTP {code}")

    results: Dict[int, int] = {}
    lock = threading.Lock()

    def hammer() -> None:
        try:
            status = get(base, "/api/state")[0]
        except (urllib.error.URLError, OSError):
            status = 0
        with lock:
            results[status] = results.get(status, 0) + 1

    threads = [threading.Thread(target=hammer) for _ in range(12)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(REQUEST_TIMEOUT * 2)
    report.step(results.get(200) == len(threads), "12 concurrent reads all answer 200",
                str(results))

    code = get(base, "/%2e%2e/README.md")[0]
    report.step(code == 404, "a traversal attempt answers 404", f"HTTP {code}")

    code, body, _ = get(base, "/api/missing")
    report.step(code == 404 and b"not found" in body, "an unknown route answers a JSON 404",
                f"HTTP {code}")


def surface_proof(report: Report, log) -> None:
    """The UI inventory proof runs and reports its surface, as the UI guard expects."""
    done = subprocess.run([sys.executable, str(ROOT / "tools" / "ui_inventory.py")],
                          capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
                          cwd=str(ROOT))
    log.write(done.stdout + done.stderr)
    entries = [line for line in done.stdout.splitlines() if line.strip()]
    report.step(done.returncode == 0 and len(entries) >= 20,
                "the UI inventory proof reports its surface", f"{len(entries)} entries")


def main() -> int:
    """Run both tracks in one sandbox and print at most 15 lines."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = Report()
    before = fingerprint()
    with tempfile.TemporaryDirectory(prefix="fold-dogfood-") as box:
        with open(LOG_PATH, "w", encoding="utf-8") as log:
            port = free_port()
            base = f"http://127.0.0.1:{port}"
            command = [sys.executable, str(ROOT / "run.py"), "--port", str(port),
                       "--seed", "7"]
            alive = False
            with supervised(command, log) as process:
                if wait_until_serving(base):
                    report.step(True, "the server starts and answers", base)
                    golden_path(base, report)
                    chaos(base, report)
                else:
                    report.step(False, "the server starts and answers",
                                f"no answer within {START_TIMEOUT:.0f}s")
                alive = process.poll() is None
                log.write(f"\nsandbox={box}\n")
            report.step(alive, "the server survived every hostile input")
            surface_proof(report, log)
            log.write("\n".join(report.lines) + "\n")

    report.step(fingerprint() == before, "the run left the tracked tree untouched")
    passed = len(report.lines) - len(report.failures)
    print(f"FOLD DOGFOOD (PRINCIPLE-015): {passed}/{len(report.lines)} steps passed")
    for failure in report.failures[:MAX_REPORT_LINES - 4]:
        print(f"  [FAIL] {failure}")
    print(f"  full log: {LOG_PATH.relative_to(ROOT).as_posix()}")
    if report.failures:
        print("Why: the product must work and hold up under hostile input before it ships.")
        print("Fix: read the log, fix the failing step, then rerun this command.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
