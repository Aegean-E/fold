# fold

[![Built with AIKit](https://img.shields.io/badge/built%20with-AIKit-6f42c1)](https://github.com/AegeanWorks/AIKit)

A small 4x4 tile-merge game you run on your own machine: one Python process, a browser
page, no third-party dependencies, no account and no network calls. Slide the grid, join
matching tiles, and chase 2048. The server owns the rules; the browser only renders the
snapshot it returns.

## 30-Second Cold-Start Quick Reference

- **Runtime Prerequisites**: Python 3.9+ (standard library only, nothing to install) and any
  modern browser with `fetch` support.
- **Start it**:
  ```bash
  python run.py            # then open http://127.0.0.1:8766
  ```
- **Canonical Regression Shield Gate**:
  ```bash
  python -m unittest discover -s tests -t .
  ```
- **UI inventory proof** (the snapshot the UI guard compares against):
  ```bash
  python tools/ui_inventory.py
  ```
- **Dogfood gate** (starts the real server, plays it, then attacks it):
  ```bash
  python tools/dogfood.py
  ```

### AIKit Commands (run from the AIKit folder)

| Role | Command |
|---|---|
| Status, task and gates | `python aikit.py status fold` |
| Phase 4: every gate | `python aikit.py check fold` |
| Repair memory and map, then check | `python aikit.py fix fold` |
| Resume an interrupted task | `python aikit.py resume fold` |
| Open a bounded UI task | `python aikit.py ui begin fold --surface web` |
| Check scope, proofs and style | `python aikit.py ui verify fold` |

## What's Inside

```text
fold/
├── .gitattributes            <- launcher line-ending policy
├── play.bat                  <- double-click launcher for Windows
├── play.command              <- double-click launcher for macOS
├── play.sh                   <- launcher for macOS and Linux terminals
├── start.bat                 <- Windows alias for play.bat
├── start.command             <- macOS alias for play.command
├── start.sh                  <- POSIX alias for play.sh
├── run.py                    <- entry point: prints the URL and serves
├── pyproject.toml            <- stack marker; no runtime dependencies
├── fold/
│   ├── __init__.py           <- package marker and version
│   ├── __main__.py           <- `python -m fold` entry point
│   ├── board.py              <- pure slide, merge, spawn and terminal rules
│   ├── game.py               <- one in-memory game: score, undo, read model
│   ├── server.py             <- stdlib HTTP: web/ plus four JSON endpoints
│   └── cli.py                <- flags, port validation, clean stop
├── web/
│   ├── index.html            <- the page: scores, board, controls, live region
│   ├── favicon.svg           <- the tab mark
│   ├── theme.css             <- every colour, font and type token
│   ├── app.css               <- layout and motion only
│   └── app.js                <- renders snapshots; keyboard and swipe helpers
├── tools/
│   ├── __init__.py           <- package marker
│   ├── ui_inventory.py       <- prints the UI inventory, one entry per line
│   └── dogfood.py            <- golden path plus hostile input over HTTP
├── tests/
│   ├── __init__.py           <- package marker
│   ├── test_board.py         <- slides, merges, spawns and terminal states
│   ├── test_game.py          <- one game's score, undo and read model
│   ├── test_server.py        <- real socket: endpoints, assets and 400s
│   ├── test_cli.py           <- local defaults, port validation and the triad
│   ├── test_inventory.py     <- controls, handlers and theme tokens stay visible
│   └── test_launchers.py     <- one-click launchers and CRLF safety
├── .gitignore                <- bytecode, caches and dogfood logs
├── README.md
├── COMMERCIAL.md
├── LICENSE
├── LICENSES/                 <- REUSE license texts
├── REUSE.toml                <- Machine-readable SPDX metadata
├── ASSETS.md                 <- Asset/data manifest: what the license covers
└── .aikit/                   <- this project's memory: record, ledger, decisions
```

## One-Click Launch

- **Windows**: double-click `play.bat` (or its `start.bat` alias).
- **macOS**: double-click `play.command` (or `start.command`); `sh play.command` works even if
  Finder has not marked the file executable.
- **Linux / terminal**: run `sh play.sh` (or `./play.sh` when the file is executable, or `sh start.sh`).

Each launcher starts `python run.py --open` on the default port, opens
http://127.0.0.1:8766, and leaves the server running in the terminal. Close the window or
press `Ctrl+C` to stop it. A failed start keeps the Windows window open so the message stays
visible. The scoreboard shows score, best and moves.

## How to Play

| Control | What it does |
|---|---|
| **Arrow keys / WASD** | Slide every tile up, down, left or right. |
| **Swipe** | The same four directions on a touch screen. |
| **New game** | Deals a fresh board and resets the score. |
| **Undo** | Restores the board and score before the last real move (up to 20 back). |
| **Keep going** | Dismisses the 2048 milestone and lets the board continue. |

A slide that moves no tile is blocked: it does not spawn a tile, score a point or charge a
move. The game ends when the grid is full and no orthogonal neighbours match. The best
score is kept in the browser's local storage; the current board lives in the server process
only, so stopping `run.py` starts a new game next time.

## Flags and Errors

`python run.py` accepts:

| Flag | Default | Meaning |
|---|---|---|
| `--port` | `8766` | Listen port, 1-65535. |
| `--host` | `127.0.0.1` | Interface to bind; loopback by default. |
| `--seed` | random | Reproducible starting board. |
| `--open` | off | Open the page in the default browser. |

A bad value exits 2 with a message from the parser; a port another process already holds
exits 1 with a `Why:` and a `Fix:`. `Ctrl+C` stops the server cleanly.

## The UI Contract

`.aikit/ui.json` bounds UI work to the `web/**` surface, protects the engine, tests, tools
and README, runs `python -m unittest discover -s tests -t .` as its fast proof, and uses
`python tools/ui_inventory.py` as its snapshot. `web/theme.css` and `web/favicon.svg` are the
declared theme paths, so a colour or font literal in `app.css` or `app.js` is a mechanical
style finding.
The contract lives in `.aikit/ui.json`; `ui_required` is false until the surface has a
finished UI task, so every gate can run before the UI evidence task is committed.

## Verification

- `python -m unittest discover -s tests -t .` runs 46 unit and socket tests without a
  browser or a network call beyond loopback.
- `python tools/dogfood.py` starts a real server on a free port, checks the page's controls,
  makes and undoes a move, then sends malformed JSON, a bad direction, an oversized body,
  concurrent reads and a traversal attempt.
- `python aikit.py check fold` runs the test, dogfood, hygiene, guidelines and secret gates.
  The guidelines gate regenerates `.aikit/codebase_map.md` from the AST.

## Design

The engine is pure and takes its random source as an argument, so every rule is testable
without a clock, a socket or a browser. The HTTP layer translates requests into `Game`
calls and serializes mutations behind one lock. All web colour and type live in
`web/theme.css`, with the favicon declared as theme art; `web/app.css` carries layout only.
Every response also carries a same-origin CSP, `nosniff`, `no-referrer` and a same-origin
resource policy. The snapshot proof is a parsed inventory of ids,
actions, roles, live regions, handlers and theme tokens rather than a screenshot, because
the project declares no browser dependency. The reasoning is recorded in
`.aikit/decisions.md`.

## 📜 License

Free for personal play under the Aegean Game License 1.1 (AGL-1.1); see [LICENSE](LICENSE). It is DRM-free: Licensor ships no DRM and a distributor may not add it. Streaming, modding and free mods are allowed. Commercial use, paid mods and AI training need the Aegean Commercial License 1.0 (ACL-1.0); see [COMMERCIAL.md](COMMERCIAL.md).
