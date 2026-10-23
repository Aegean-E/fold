"""
Start Fold and print the one URL a user needs.

Standard library only, no environment variables and no prompts. The game is in memory:
stopping the process ends the session, and the next start deals a fresh grid.

PRINCIPLE-011.
"""

import argparse
import random
import sys
import webbrowser
from typing import List, Optional

from fold.game import Game
from fold.server import build_server

DEFAULT_PORT = 8766


class TriadParser(argparse.ArgumentParser):
    """Argparse that adds AIKit's Why/Fix triad to a bad flag (PRINCIPLE-011 R5)."""

    def error(self, message: str) -> None:
        """Print usage and a triad, then exit 2 without opening a socket."""
        self.print_usage(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n"
                     "Why: the flags describe how Fold should start, so a bad value is "
                     "refused before a socket opens.\n"
                     "Fix: use --port 1-65535, --host 127.0.0.1, and a whole-number --seed; "
                     "--help lists them.\n")


def port_number(text: str) -> int:
    """Argparse type for a TCP port, with a message a person can act on."""
    try:
        port = int(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError("port must be a whole number") from error
    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
    return port


def parse_args(argv: List[str]) -> argparse.Namespace:
    """The command line: local host, port, optional seed and optional browser open."""
    parser = TriadParser(
        prog="python run.py", description="Run Fold, a local tile-merge game.")
    parser.add_argument("--port", type=port_number, default=DEFAULT_PORT,
                        help=f"port to listen on (default: {DEFAULT_PORT})")
    parser.add_argument("--host", default="127.0.0.1",
                        help="interface to bind (default: 127.0.0.1)")
    parser.add_argument("--seed", type=int, default=None,
                        help="make the initial board reproducible")
    parser.add_argument("--open", action="store_true",
                        help="open the page in the default browser after starting")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Serve until interrupted; 0 on a clean stop, 1 on a bind failure, 2 on bad flags."""
    args = parse_args(sys.argv[1:] if argv is None else argv)
    game = Game(random.Random(args.seed) if args.seed is not None else None)
    try:
        server = build_server(game, args.port, host=args.host)
    except OSError as error:
        print(f"could not listen on {args.host}:{args.port}: {error}", file=sys.stderr)
        print("Why: another process already holds that port, or the interface is unavailable.",
              file=sys.stderr)
        print("Fix: stop it, or start Fold with --port <other> and --host 127.0.0.1.",
              file=sys.stderr)
        return 1
    host, port = server.server_address[0], server.server_address[1]
    display_host = "127.0.0.1" if host in ("0.0.0.0", "::") else host
    url = f"http://{display_host}:{port}"
    print(f"Fold is running at {url}  (Ctrl+C to stop)")
    if args.open:
        webbrowser.open_new_tab(url)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        print("\nFold stopped.")
    finally:
        server.server_close()
    return 0
