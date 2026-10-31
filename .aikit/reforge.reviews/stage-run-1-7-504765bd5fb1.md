Review one Git audit stage. Report two kinds of item, both tied to the change.

kind "defect": something the change introduces or leaves in a worse state. A bug, a wrong condition,
a missing guard, a swallowed error, a documented promise the code does not keep.

kind "improvement": a concrete gap or better implementation in the code the change touches. A case
the new code does not handle, a missing test for a new branch, a simpler correct approach, an API
that forces callers to repeat work. Improvements must be specific and actionable, with a line you
can point at. Never report pure style or naming taste.

Do not invent files or lines. Do not propose work unrelated to the diff.

Return one JSON object:
{"findings": [{"path": "relative/path", "line": 12, "severity": "high|medium|low",
  "kind": "defect|improvement", "commit": "commit sha", "hunk": "hunk id",
  "code": "short-kebab-case", "message": "what is wrong or missing, and why it matters",
  "evidence": "the exact changed line or a short quote",
  "fix": {"old": "exact text that appears once in the file", "new": "replacement text"}}],
 "reviewed_hunks": ["hunk id", "..."]}

`reviewed_hunks` is optional; when supplied it records which packet hunks were actually read.
`commit` and `hunk` are optional; when present they must name a commit and hunk shown in this
packet. They keep a finding attributed to the change that introduced it. `fix` is optional. Include it only when the replacement is exact, minimal and safe. Use the file's
real line endings and whitespace in `old`. An empty findings list is a valid answer.

Read the unified diff as it is: a line starting with `+` exists after the commit, a line starting
with `-` was removed by it and is NOT in the file, and a leading space marks unchanged context.
Every `evidence` must quote a line that exists in the file after the change, verbatim. Never report
a removed line as a current problem.

The packet lists every new commit oldest to newest, with that commit's own hunks. A later commit
may correct or replace an earlier hunk, so judge the current file: every `evidence` must quote a
line that still exists, verbatim, and a suggested replacement must land on a line one of these
commits added. A binary file is named at the end because it cannot be reviewed as text.

Stage 7 (window 21), commits (root commit)..504765bd5fb1
Changed text files: .aikit/codebase_map.md, .aikit/decisions.md, .aikit/guidelines.md, .aikit/project.json, .aikit/ui.json, .gitattributes, .gitignore, README.md, fold/__init__.py, fold/__main__.py, fold/board.py, fold/cli.py, fold/game.py, fold/server.py, play.bat, play.command, play.sh, pyproject.toml, run.py, start.bat, start.command, start.sh, tests/__init__.py, tests/test_board.py, tests/test_cli.py, tests/test_game.py, tests/test_inventory.py, tests/test_launchers.py, tests/test_server.py, tools/__init__.py, tools/dogfood.py, tools/ui_inventory.py, web/app.css, web/app.js, web/favicon.svg, web/index.html, web/theme.css
### Hunk manifest
- 50f0d58bcca6 chore: start project with AIKit memory: 5 hunk(s)
- 251bece542b0 feat(fold): add zero-dependency tile-merge game: 36 hunk(s)

### commit 50f0d58bcca6 chore: start project with AIKit memory
--- .aikit/decisions.md ---
hunk 50f0d58bcca6:.aikit/decisions.md#1 (new lines 1..13)
@@ -0,0 +1,13 @@
+# Decisions
+
+Why this project is built the way it is, oldest first. One entry per decision that changes a
+contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.
+
+<!-- Entry format:
+### ADR-NNN: <decision in one line>
+- **Date**: YYYY-MM-DD
+- **Status**: Accepted
+- **Context**: <what forced the decision>
+- **Decision**: <what was decided>
+- **Consequences**: <what follows, including what it costs>
+-->
--- .aikit/guidelines.md ---
hunk 50f0d58bcca6:.aikit/guidelines.md#1 (new lines 1..11)
@@ -0,0 +1,11 @@
+# Project Guidelines
+
+Rules for this project only, written by people or AI agents. They add to AIKit's principles and
+rank below them: a guideline never overrides a principle (PRINCIPLE-000 R6, PRINCIPLE-001 R4).
+Add one with `python aikit.py guideline <name> "<rule>" --source <user|ADR-NNN|person>`, or by
+hand as one line below in the form `- **G-NNN** (source): rule`; IDs are never reused.
+
+Persisted state carries a format version. A loader refuses a version it does not support,
+without modifying or quarantining that file; older versions migrate when a migration exists.
+
+## Rules
--- .aikit/project.json ---
hunk 50f0d58bcca6:.aikit/project.json#1 (new lines 1..8)
@@ -0,0 +1,8 @@
+{
+  "schema": 1,
+  "name": "fold",
+  "test_command": "python -m unittest discover -s tests -t .",
+  "gates": {},
+  "ui_required": false,
+  "created": "2026-10-22"
+}
\ No newline at end of file
--- .gitignore ---
hunk 50f0d58bcca6:.gitignore#1 (new lines 1..8)
@@ -0,0 +1,8 @@
+# AIKit transient state
+.aikit/*.lock
+.aikit/*.bak
+.aikit/*.tmp_*
+.aikit/*.corrupt_*
+__pycache__/
+*.py[cod]
+node_modules/
--- README.md ---
hunk 50f0d58bcca6:README.md#1 (new lines 1..26)
@@ -0,0 +1,26 @@
+# fold
+
+## ⚡ 30-Second Cold-Start Quick Reference
+
+- **Runtime Prerequisites**: <FILL: each runtime this project needs and its minimum version>
+- **Canonical Regression Shield Gate**:
+  ```bash
+  python -m unittest discover -s tests -t .
+  ```
+
+### 🛠️ AIKit Commands (run from the AIKit folder)
+| Role | Command |
+|---|---|
+| Status, task and gates | `python aikit.py status fold` |
+| Phase 4: every gate | `python aikit.py check fold` |
+| Repair memory and map, then check | `python aikit.py fix fold` |
+| Resume an interrupted task | `python aikit.py resume fold` |
+
+## 📦 What's Inside
+
+```text
+fold/
+├── .gitignore                <- transient AIKit state excluded
+├── README.md
+└── .aikit/                   <- this project's memory: record, ledger, decisions
+```

### commit 251bece542b0 feat(fold): add zero-dependency tile-merge game
--- .aikit/codebase_map.md ---
hunk 251bece542b0:.aikit/codebase_map.md#1 (new lines 1..287)
@@ -0,0 +1,287 @@
+# Codebase Map & Symbol Catalog 🗺️
+
+> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
+> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.
+
+---
+
+## 📊 Codebase Metrics
+- **Total Python Modules**: `17`
+- **Total Classes**: `18`
+- **Total Top-Level Functions**: `29`
+- **Total Class Methods**: `72`
+- **Total Source Lines**: `1283`
+
+---
+
+## 📦 Modules & Exported Symbols
+
+### [`fold/__init__.py`](fold/__init__.py)
+> *Fold: a small 4x4 tile-merge game with a local browser surface.*
+
+**Size**: `3` lines (`93` bytes)
+
+---
+
+### [`fold/__main__.py`](fold/__main__.py)
+> *Allow `python -m fold` as the same entry point as `python run.py`.*
+
+**Size**: `8` lines (`161` bytes)
+
+---
+
+### [`fold/board.py`](fold/board.py)
+> *The pure board rules of Fold.*
+
+**Size**: `121` lines (`4106` bytes)
+
+**Functions:**
+- `def empty_board()` - *A 4x4 board with no tiles.*
+- `def slide_row(row)` - *Slide one row toward index zero, merging equal neighbours once, left to right.*
+- `def move(board, direction)` - *Slide every tile in `direction`; return the new board and the points earned.*
+- `def spawn(board, rng, count)` - *Place `count` new tiles (90% a 2, 10% a 4) in empty cells chosen by `rng`.*
+- `def has_won(board, target)` - *Whether any tile has reached the winning value.*
+- `def has_moves(board)` - *Whether an empty cell or an equal orthogonal neighbour leaves a move available.*
+- `def _slide_rows(board)` - *Slide every row toward index zero and sum the points.*
+- `def _transpose(board)` - *Swap rows and columns.*
+- `def _flip_rows(board)` - *Mirror every row left to right.*
+
+---
+
+### [`fold/cli.py`](fold/cli.py)
+> *Start Fold and print the one URL a user needs.*
+
+**Size**: `86` lines (`3461` bytes)
+
+**Classes:**
+- `class TriadParser` - *Argparse that adds AIKit's Why/Fix triad to a bad flag (PRINCIPLE-011 R5).*
+  - Method `.error(message)` - *Print usage and a triad, then exit 2 without opening a socket.*
+
+**Functions:**
+- `def port_number(text)` - *Argparse type for a TCP port, with a message a person can act on.*
+- `def parse_args(argv)` - *The command line: local host, port, optional seed and optional browser open.*
+- `def main(argv)` - *Serve until interrupted; 0 on a clean stop, 1 on a bind failure, 2 on bad flags.*
+
+---
+
+### [`fold/game.py`](fold/game.py)
+> *One game in memory: a board, a score, and a short undo trail.*
+
+**Size**: `84` lines (`3117` bytes)
+
+**Classes:**
+- `class Game` - *A tile-merge game with one-level-or-more undo and a JSON-ready read model.*
+  - Method `.__init__(rng, board)`
+  - Method `.reset()` - *Start a fresh game with two tiles and no undo history.*
+  - Method `.move(direction)` - *Apply one direction, spawn one tile after a real move, and report the outcome.*
+  - Method `.undo()` - *Restore the board and score before the last real move, if there is one.*
+  - Method `.state(moved, gained)` - *The flat read model the HTTP layer and the browser both consume.*
+  - Method `._starting_board()` - *Two tiles placed by the game's own random source.*
+  - Method `._remember()` - *Keep the pre-move state for undo, bounded so a long game cannot grow forever.*
+
+---
+
+### [`fold/server.py`](fold/server.py)
+> *The local HTTP layer: static files from `web/` and four JSON endpoints.*
+
+**Size**: `168` lines (`6578` bytes)
+
+**Classes:**
+- `class StaticFiles` - *Resolves a URL path to a file inside one directory, and never outside it.*
+  - Method `.resolve(url_path)` - *The file a decoded URL path names, or None when it escapes or does not exist.*
+- `class FoldHandler` - *Translates requests into `Game` reads and mutations.*
+  - Method `.do_GET()`
+  - Method `.do_POST()`
+  - Method `._payload(raw)` - *Decode one JSON object; anything else is a 400, never a traceback.*
+  - Method `._act(route, payload)` - *Apply one named endpoint to the game and return its read model.*
+  - Method `._json(status, payload)`
+  - Method `._respond(status, content_type, body, cache)`
+  - Method `.end_headers()` - *Attach the security policy to every response, including stdlib errors.*
+  - Method `.log_message(format, *args)` - *Silent by default; `fold.cli` prints the one line a user needs.*
+- `class FoldHTTPServer` - *A local thread-per-request server whose threads do not outlive the process.*
+
+**Functions:**
+- `def build_server(game, port, web, host)` - *An HTTP server bound to `host:port`, serving `web` and one in-memory game.*
+
+---
+
+### [`run.py`](run.py)
+> *The user-facing entry point: `python run.py` starts Fold on port 8766.*
+
+**Size**: `9` lines (`188` bytes)
+
+---
+
+### [`tests/__init__.py`](tests/__init__.py)
+> *Fold's test package.*
+
+**Size**: `1` lines (`27` bytes)
+
+---
+
+### [`tests/test_board.py`](tests/test_board.py)
+> *Pure board rules: sliding, merging, spawning and terminal detection.*
+
+**Size**: `85` lines (`3398` bytes)
+
+**Classes:**
+- `class SlideRowTest`
+  - Method `.test_equal_neighbours_merge_once_and_earn_their_sum()`
+  - Method `.test_zeros_compact_before_merging()`
+  - Method `.test_a_merged_tile_never_merges_again_in_the_same_slide()`
+  - Method `.test_a_row_with_no_pair_only_compacts()`
+- `class MoveTest`
+  - Method `.test_left_and_right_are_mirror_images()`
+  - Method `.test_up_and_down_are_mirror_images()`
+  - Method `.test_an_unknown_direction_is_refused()`
+- `class SpawnTest`
+  - Method `.test_spawn_places_the_requested_number_of_tiles_in_empty_cells()`
+  - Method `.test_spawn_with_a_shared_seed_is_replayable()`
+  - Method `.test_spawn_never_overwrites_a_tile()`
+- `class TerminalTest`
+  - Method `.test_winning_value_is_detected()`
+  - Method `.test_an_empty_cell_leaves_a_move()`
+  - Method `.test_a_full_checkerboard_has_no_moves()`
+  - Method `.test_a_full_board_with_an_equal_neighbour_still_moves()`
+
+---
+
+### [`tests/test_cli.py`](tests/test_cli.py)
+> *Command-line parsing: local defaults, an optional seed and a validated port.*
+
+**Size**: `44` lines (`1387` bytes)
+
+**Classes:**
+- `class CliTest`
+  - Method `.test_defaults_keep_the_game_local()`
+  - Method `.test_a_seed_and_open_are_opt_in()`
+  - Method `.test_a_port_outside_the_valid_range_is_refused()`
+  - Method `.test_a_valid_port_is_an_integer()`
+  - Method `.test_a_bad_flag_exits_two_with_a_triad()`
+
+---
+
+### [`tests/test_game.py`](tests/test_game.py)
+> *One game's state transitions: start, move, undo and terminal read model.*
+
+**Size**: `82` lines (`3244` bytes)
+
+**Classes:**
+- `class GameTest`
+  - Method `.test_a_new_game_has_two_tiles_and_no_history()`
+  - Method `.test_a_move_merges_scores_and_spawns_exactly_one_tile()`
+  - Method `.test_a_blocked_direction_changes_nothing()`
+  - Method `.test_undo_restores_the_board_and_score()`
+  - Method `.test_reset_deals_a_new_board_and_clears_history()`
+  - Method `.test_a_full_checkerboard_reports_game_over()`
+  - Method `.test_a_2048_tile_reports_a_win()`
+  - Method `.test_state_has_the_declared_json_shape()`
+
+---
+
+### [`tests/test_inventory.py`](tests/test_inventory.py)
+> *The UI inventory proof covers the controls, handlers, live region and theme tokens.*
+
+**Size**: `29` lines (`983` bytes)
+
+**Classes:**
+- `class InventoryTest`
+  - Method `.test_the_inventory_names_the_controls_and_theme_tokens()`
+  - Method `.test_the_page_and_script_are_part_of_the_surface()`
+
+---
+
+### [`tests/test_launchers.py`](tests/test_launchers.py)
+> *One-click launch files: present, CRLF-safe on Windows and pointing at run.py.*
+
+**Size**: `45` lines (`1819` bytes)
+
+**Classes:**
+- `class LauncherTest`
+  - Method `.test_every_launcher_exists()`
+  - Method `.test_batch_files_have_crlf_line_endings()`
+  - Method `.test_launchers_start_the_game_and_aliases_delegate()`
+  - Method `.test_a_batch_failure_stays_visible()`
+  - Method `.test_gitattributes_pins_launcher_line_endings()`
+
+---
+
+### [`tests/test_server.py`](tests/test_server.py)
+> *The HTTP layer over a real socket: JSON endpoints, static files and hostile input.*
+
+**Size**: `138` lines (`5734` bytes)
+
+**Classes:**
+- `class ServerHarness` - *One server on an ephemeral port, torn down without a lingering thread.*
+  - Method `.__init__(board)`
+  - Method `.close()`
+  - Method `.request(path, payload)`
+- `class ServerTest`
+  - Method `.setUp()`
+  - Method `.test_the_page_and_assets_are_served()`
+  - Method `.test_security_headers_are_present()`
+  - Method `.test_state_returns_the_declared_shape()`
+  - Method `.test_a_move_merges_and_spawns_a_tile()`
+  - Method `.test_undo_restores_the_previous_board()`
+  - Method `.test_a_bad_direction_is_a_400_with_an_error()`
+  - Method `.test_malformed_json_is_a_400()`
+  - Method `.test_an_oversized_body_is_a_413()`
+  - Method `.test_an_unknown_route_is_a_json_404()`
+  - Method `.test_a_trailing_slash_is_not_the_index()`
+- `class StaticFilesTest`
+  - Method `.setUp()`
+  - Method `.test_root_serves_the_index()`
+  - Method `.test_paths_outside_the_web_root_are_refused()`
+
+---
+
+### [`tools/__init__.py`](tools/__init__.py)
+> *Developer proofs for Fold.*
+
+**Size**: `1` lines (`33` bytes)
+
+---
+
+### [`tools/dogfood.py`](tools/dogfood.py)
+> *Fold's dogfood runner: play it the way a user does, then attack the surface.*
+
+**Size**: `278` lines (`11372` bytes)
+
+**Classes:**
+- `class Report` - *Collects step outcomes: the console sees a summary, the log sees everything.*
+  - Method `.__init__()`
+  - Method `.step(ok, label, detail)` - *Record one step's outcome and hand back whether it passed.*
+
+**Functions:**
+- `def terminate_process_tree(process)` - *Kill a process and everything it started, on Windows and POSIX alike.*
+- `def supervised(command, log)` - *Run a command with stdin closed, killing its whole tree on the way out.*
+- `def free_port()` - *A port the operating system says is free right now.*
+- `def fingerprint()` - *A digest of every tracked file, so a run that dirties the repository fails.*
+- `def get(base, path)` - *One GET, with the milliseconds it took.*
+- `def post(base, path, payload, raw)` - *One POST; an HTTP error is an answer here, not an exception.*
+- `def wait_until_serving(base)` - *True once the server answers, False if it never does within the start timeout.*
+- `def golden_path(base, report)` - *Load the page, make a move, undo it and read the state back.*
+- `def chaos(base, report)` - *Hostile input: malformed JSON, bad directions, a flood and traversal.*
+- `def surface_proof(report, log)` - *The UI inventory proof runs and reports its surface, as the UI guard expects.*
+- `def main()` - *Run both tracks in one sandbox and print at most 15 lines.*
+
+---
+
+### [`tools/ui_inventory.py`](tools/ui_inventory.py)
+> *Print Fold's UI inventory, one entry per line.*
+
+**Size**: `101` lines (`3666` bytes)
+
+**Classes:**
+- `class SurfaceParser` - *Collects identified elements, named actions and live regions of one page.*
+  - Method `.__init__()`
+  - Method `.handle_starttag(tag, attrs)`
+
+**Functions:**
+- `def html_entries(path)` - *Identified elements, actions, roles and live regions declared in a page.*
+- `def handler_entries(path)` - *Action names the browser script is willing to dispatch.*
+- `def token_entries(path)` - *Theme custom properties the stylesheet declares.*
+- `def inventory(web)` - *Every inventory entry of a web directory, sorted and deduplicated.*
+- `def main(argv)` - *Write the inventory to stdout; exit 1 when the surface has no entries at all.*
+
+---
--- .aikit/decisions.md ---
hunk 251bece542b0:.aikit/decisions.md#1 (new lines 11..41)
@@ -11,3 +11,31 @@ contract, a dependency, a data format or the architecture; IDs are consecutive a
 - **Decision**: <what was decided>
 - **Consequences**: <what follows, including what it costs>
 -->
+
+### ADR-001: The server owns the rules; the browser owns only the rendering
+- **Date**: 2026-10-22
+- **Status**: Accepted
+- **Context**: A tile-merge game has enough rules (merge-once, spawn, score, win, game over) that a second browser implementation would drift from the tested one.
+- **Decision**: `fold/board.py` holds pure rules and `fold/game.py` holds one game's state and undo trail. `fold/server.py` translates four JSON endpoints into those calls; `web/app.js` renders the returned snapshot and posts a direction.
+- **Consequences**: Every rule is tested in Python without a browser, and a reload cannot show a board the rules would reject. The cost is one loopback round trip per move, which is negligible for a turn-based local game.
+
+### ADR-002: One lock serializes game mutations on a threaded local server
+- **Date**: 2026-10-22
+- **Status**: Accepted
+- **Context**: The browser can issue a move while another tab polls the state, and a race could spawn two tiles or lose an undo entry.
+- **Decision**: `FoldHTTPServer` is thread-per-request, while every `Game` read and mutation runs under one `threading.Lock` held by the request handler.
+- **Consequences**: State transitions are atomic and the game stays simple; concurrent reads serialize for microseconds. The lock is not a persistence layer: the game vanishes when the process stops.
+
+### ADR-003: The snapshot proof is a parsed inventory, not a rendered screenshot
+- **Date**: 2026-10-22
+- **Status**: Accepted
+- **Context**: The UI guard needs a stable way to notice a dropped control, action, handler or theme token, but Fold declares no browser or Node dependency.
+- **Decision**: `tools/ui_inventory.py` parses `web/` and prints one line per identified element, named action, ARIA role, live region, script handler and theme token. `tools/dogfood.py` covers the served page and the API over a real socket.
+- **Consequences**: A dropped control or token is a lost inventory line and accessibility attributes are guarded alongside controls. A purely visual regression that keeps the inventory intact is not caught; that is the deliberate price of a zero-dependency surface.
+
+### ADR-004: Fold listens on 8766, not the workspace's other local port
+- **Date**: 2026-10-23
+- **Status**: Accepted
+- **Context**: A previous local server process can keep port 8765 open for hours. Fold's old default collided with it, so opening `http://127.0.0.1:8765` showed that other application instead of the game, and the browser had no way to tell the difference.
+- **Decision**: `DEFAULT_PORT` is `8766`. The port stays fixed, so the browser's local-storage best score remains on one origin, and `--port` still accepts any free port from 1 to 65535.
+- **Consequences**: One-click launchers open Fold without a collision when the other local tool owns 8765. A second Fold instance on 8766 exits with a Why/Fix message instead of opening a different page; the same message appears for any other occupied port.
--- .aikit/project.json ---
hunk 251bece542b0:.aikit/project.json#1 (new lines 2..10)
@@ -2,7 +2,9 @@
   "schema": 1,
   "name": "fold",
   "test_command": "python -m unittest discover -s tests -t .",
-  "gates": {},
+  "gates": {
+    "dogfood": "python tools/dogfood.py"
+  },
   "ui_required": false,
   "created": "2026-10-22"
 }
\ No newline at end of file
--- .aikit/ui.json ---
hunk 251bece542b0:.aikit/ui.json#1 (new lines 1..38)
@@ -0,0 +1,38 @@
+{
+  "schema": 1,
+  "surfaces": {
+    "web": {
+      "paths": [
+        "web/**"
+      ]
+    }
+  },
+  "protected": [
+    "tests/**",
+    "fold/**",
+    "tools/**",
+    "run.py",
+    "play.bat",
+    "play.command",
+    "play.sh",
+    "start.bat",
+    "start.command",
+    "start.sh",
+    "README.md",
+    ".aikit/**"
+  ],
+  "commands": {
+    "fast": "python -m unittest discover -s tests -t .",
+    "snapshot": "python tools/ui_inventory.py"
+  },
+  "style": {
+    "theme_paths": [
+      "web/theme.css",
+      "web/favicon.svg"
+    ]
+  },
+  "limits": {
+    "max_files": 12,
+    "max_lines": 300
+  }
+}
\ No newline at end of file
--- .gitattributes ---
hunk 251bece542b0:.gitattributes#1 (new lines 1..6)
@@ -0,0 +1,6 @@
+# Keep launch scripts native on every checkout.
+* text=auto
+*.bat text eol=crlf
+*.cmd text eol=crlf
+*.sh text eol=lf
+*.command text eol=lf
--- .gitignore ---
hunk 251bece542b0:.gitignore#1 (new lines 5..10)
@@ -5,4 +5,6 @@
 .aikit/*.corrupt_*
 __pycache__/
 *.py[cod]
+.pytest_cache/
 node_modules/
+.aikit/*.log
--- README.md ---
hunk 251bece542b0:README.md#1 (new lines 1..154)
@@ -1,26 +1,154 @@
 # fold
 
-## ⚡ 30-Second Cold-Start Quick Reference
+A small 4x4 tile-merge game you run on your own machine: one Python process, a browser
+page, no third-party dependencies, no account and no network calls. Slide the grid, join
+matching tiles, and chase 2048. The server owns the rules; the browser only renders the
+snapshot it returns.
 
-- **Runtime Prerequisites**: <FILL: each runtime this project needs and its minimum version>
+## 30-Second Cold-Start Quick Reference
+
+- **Runtime Prerequisites**: Python 3.9+ (standard library only, nothing to install) and any
+  modern browser with `fetch` support.
+- **Start it**:
+  ```bash
+  python run.py            # then open http://127.0.0.1:8766
+  ```
 - **Canonical Regression Shield Gate**:
   ```bash
   python -m unittest discover -s tests -t .
   ```
+- **UI inventory proof** (the snapshot the UI guard compares against):
+  ```bash
+  python tools/ui_inventory.py
+  ```
+- **Dogfood gate** (starts the real server, plays it, then attacks it):
+  ```bash
+  python tools/dogfood.py
+  ```
+
+### AIKit Commands (run from the AIKit folder)
 
-### 🛠️ AIKit Commands (run from the AIKit folder)
 | Role | Command |
 |---|---|
 | Status, task and gates | `python aikit.py status fold` |
 | Phase 4: every gate | `python aikit.py check fold` |
 | Repair memory and map, then check | `python aikit.py fix fold` |
 | Resume an interrupted task | `python aikit.py resume fold` |
+| Open a bounded UI task | `python aikit.py ui begin fold --surface web` |
+| Check scope, proofs and style | `python aikit.py ui verify fold` |
 
-## 📦 What's Inside
+## What's Inside
 
 ```text
 fold/
-├── .gitignore                <- transient AIKit state excluded
+├── .gitattributes            <- launcher line-ending policy
+├── play.bat                  <- double-click launcher for Windows
+├── play.command              <- double-click launcher for macOS
+├── play.sh                   <- launcher for macOS and Linux terminals
+├── start.bat                 <- Windows alias for play.bat
+├── start.command             <- macOS alias for play.command
+├── start.sh                  <- POSIX alias for play.sh
+├── run.py                    <- entry point: prints the URL and serves
+├── pyproject.toml            <- stack marker; no runtime dependencies
+├── fold/
+│   ├── __init__.py           <- package marker and version
+│   ├── __main__.py           <- `python -m fold` entry point
+│   ├── board.py              <- pure slide, merge, spawn and terminal rules
+│   ├── game.py               <- one in-memory game: score, undo, read model
+│   ├── server.py             <- stdlib HTTP: web/ plus four JSON endpoints
+│   └── cli.py                <- flags, port validation, clean stop
+├── web/
+│   ├── index.html            <- the page: scores, board, controls, live region
+│   ├── favicon.svg           <- the tab mark
+│   ├── theme.css             <- every colour, font and type token
+│   ├── app.css               <- layout and motion only
+│   └── app.js                <- renders snapshots; keyboard and swipe helpers
+├── tools/
+│   ├── __init__.py           <- package marker
+│   ├── ui_inventory.py       <- prints the UI inventory, one entry per line
+│   └── dogfood.py            <- golden path plus hostile input over HTTP
+├── tests/
+│   ├── __init__.py           <- package marker
+│   ├── test_board.py         <- slides, merges, spawns and terminal states
+│   ├── test_game.py          <- one game's score, undo and read model
+│   ├── test_server.py        <- real socket: endpoints, assets and 400s
+│   ├── test_cli.py           <- local defaults, port validation and the triad
+│   ├── test_inventory.py     <- controls, handlers and theme tokens stay visible
+│   └── test_launchers.py     <- one-click launchers and CRLF safety
+├── .gitignore                <- bytecode, caches and dogfood logs
 ├── README.md
 └── .aikit/                   <- this project's memory: record, ledger, decisions
 ```
+
+## One-Click Launch
+
+- **Windows**: double-click `play.bat` (or its `start.bat` alias).
+- **macOS**: double-click `play.command` (or `start.command`); `sh play.command` works even if
+  Finder has not marked the file executable.
+- **Linux / terminal**: run `sh play.sh` (or `./play.sh` when the file is executable, or `sh start.sh`).
+
+Each launcher starts `python run.py --open` on the default port, opens
+http://127.0.0.1:8766, and leaves the server running in the terminal. Close the window or
+press `Ctrl+C` to stop it. A failed start keeps the Windows window open so the message stays
+visible. The scoreboard shows score, best and moves.
+
+## How to Play
+
+| Control | What it does |
+|---|---|
+| **Arrow keys / WASD** | Slide every tile up, down, left or right. |
+| **Swipe** | The same four directions on a touch screen. |
+| **New game** | Deals a fresh board and resets the score. |
+| **Undo** | Restores the board and score before the last real move (up to 20 back). |
+| **Keep going** | Dismisses the 2048 milestone and lets the board continue. |
+
+A slide that moves no tile is blocked: it does not spawn a tile, score a point or charge a
+move. The game ends when the grid is full and no orthogonal neighbours match. The best
+score is kept in the browser's local storage; the current board lives in the server process
+only, so stopping `run.py` starts a new game next time.
+
+## Flags and Errors
+
+`python run.py` accepts:
+
+| Flag | Default | Meaning |
+|---|---|---|
+| `--port` | `8766` | Listen port, 1-65535. |
+| `--host` | `127.0.0.1` | Interface to bind; loopback by default. |
+| `--seed` | random | Reproducible starting board. |
+| `--open` | off | Open the page in the default browser. |
+
+A bad value exits 2 with a message from the parser; a port another process already holds
+exits 1 with a `Why:` and a `Fix:`. `Ctrl+C` stops the server cleanly.
+
+## The UI Contract
+
+`.aikit/ui.json` bounds UI work to the `web/**` surface, protects the engine, tests, tools
+and README, runs `python -m unittest discover -s tests -t .` as its fast proof, and uses
+`python tools/ui_inventory.py` as its snapshot. `web/theme.css` and `web/favicon.svg` are the
+declared theme paths, so a colour or font literal in `app.css` or `app.js` is a mechanical
+style finding.
+The contract lives in `.aikit/ui.json`; `ui_required` is false until the surface has a
+finished UI task, so every gate can run before the UI evidence task is committed.
+
+## Verification
+
+- `python -m unittest discover -s tests -t .` runs 46 unit and socket tests without a
+  browser or a network call beyond loopback.
+- `python tools/dogfood.py` starts a real server on a free port, checks the page's controls,
+  makes and undoes a move, then sends malformed JSON, a bad direction, an oversized body,
+  concurrent reads and a traversal attempt.
+- `python aikit.py check fold` runs the test, dogfood, hygiene, guidelines and secret gates.
+  The guidelines gate regenerates `.aikit/codebase_map.md` from the AST.
+
+## Design
+
+The engine is pure and takes its random source as an argument, so every rule is testable
+without a clock, a socket or a browser. The HTTP layer translates requests into `Game`
+calls and serializes mutations behind one lock. All web colour and type live in
+`web/theme.css`, with the favicon declared as theme art; `web/app.css` carries layout only.
+Every response also carries a same-origin CSP, `nosniff`, `no-referrer` and a same-origin
+resource policy. The snapshot proof is a parsed inventory of ids,
+actions, roles, live regions, handlers and theme tokens rather than a screenshot, because
+the project declares no browser dependency. The reasoning is recorded in
+`.aikit/decisions.md`.
--- fold/__init__.py ---
hunk 251bece542b0:fold/__init__.py#1 (new lines 1..3)
@@ -0,0 +1,3 @@
+"""Fold: a small 4x4 tile-merge game with a local browser surface."""
+
+__version__ = "1.0.0"
--- fold/__main__.py ---
hunk 251bece542b0:fold/__main__.py#1 (new lines 1..8)
@@ -0,0 +1,8 @@
+"""Allow `python -m fold` as the same entry point as `python run.py`."""
+
+import sys
+
+from fold.cli import main
+
+if __name__ == "__main__":
+    sys.exit(main())
--- fold/board.py ---
hunk 251bece542b0:fold/board.py#1 (new lines 1..121)
@@ -0,0 +1,121 @@
+"""
+The pure board rules of Fold.
+
+A board is a tuple of four rows; zero means empty. Nothing here knows about HTTP, random
+seeds or the browser: `move` and `slide_row` are deterministic, and `spawn` takes the
+random source as an argument so a test can replay a game exactly.
+
+PRINCIPLE-003, PRINCIPLE-009, PRINCIPLE-014.
+"""
+
+import random
+from typing import List, Sequence, Tuple
+
+SIZE = 4
+WINNING_VALUE = 2048
+DIRECTIONS = ("up", "down", "left", "right")
+Board = Tuple[Tuple[int, ...], ...]
+
+
+def empty_board() -> Board:
+    """A 4x4 board with no tiles."""
+    return tuple((0,) * SIZE for _ in range(SIZE))
+
+
+def slide_row(row: Sequence[int]) -> Tuple[Tuple[int, ...], int]:
+    """
+    Slide one row toward index zero, merging equal neighbours once, left to right.
+
+    Returns the new row and the points earned. `[2, 2, 2, 2]` becomes `[4, 4, 0, 0]`
+    and earns 8; a merged tile never merges again on the same slide.
+    """
+    tiles = [value for value in row if value]
+    merged: List[int] = []
+    gained = 0
+    index = 0
+    while index < len(tiles):
+        if index + 1 < len(tiles) and tiles[index] == tiles[index + 1]:
+            value = tiles[index] * 2
+            merged.append(value)
+            gained += value
+            index += 2
+        else:
+            merged.append(tiles[index])
+            index += 1
+    merged.extend([0] * (SIZE - len(merged)))
+    return tuple(merged), gained
+
+
+def move(board: Board, direction: str) -> Tuple[Board, int]:
+    """
+    Slide every tile in `direction`; return the new board and the points earned.
+
+    An unknown direction raises `ValueError`, so a bad request never mutates a game.
+    """
+    if direction not in DIRECTIONS:
+        raise ValueError(f"direction must be one of {', '.join(DIRECTIONS)}")
+    if direction == "left":
+        return _slide_rows(board)
+    if direction == "right":
+        flipped, gained = _slide_rows(_flip_rows(board))
+        return _flip_rows(flipped), gained
+    if direction == "up":
+        transposed, gained = _slide_rows(_transpose(board))
+        return _transpose(transposed), gained
+    transposed, gained = _slide_rows(_flip_rows(_transpose(board)))
+    return _transpose(_flip_rows(transposed)), gained
+
+
+def spawn(board: Board, rng: random.Random, count: int = 1) -> Board:
+    """
+    Place `count` new tiles (90% a 2, 10% a 4) in empty cells chosen by `rng`.
+
+    When fewer empty cells exist than `count`, every empty cell is filled.
+    """
+    cells = [(row, column) for row in range(SIZE) for column in range(SIZE)
+             if board[row][column] == 0]
+    rng.shuffle(cells)
+    updated = [list(row) for row in board]
+    for row, column in cells[:max(0, count)]:
+        updated[row][column] = 4 if rng.random() < 0.1 else 2
+    return tuple(tuple(row) for row in updated)
+
+
+def has_won(board: Board, target: int = WINNING_VALUE) -> bool:
+    """Whether any tile has reached the winning value."""
+    return any(value >= target for row in board for value in row)
+
+
+def has_moves(board: Board) -> bool:
+    """Whether an empty cell or an equal orthogonal neighbour leaves a move available."""
+    for row in range(SIZE):
+        for column in range(SIZE):
+            value = board[row][column]
+            if value == 0:
+                return True
+            if column + 1 < SIZE and board[row][column + 1] == value:
+                return True
+            if row + 1 < SIZE and board[row + 1][column] == value:
+                return True
+    return False
+
+
+def _slide_rows(board: Board) -> Tuple[Board, int]:
+    """Slide every row toward index zero and sum the points."""
+    rows: List[Tuple[int, ...]] = []
+    gained = 0
+    for row in board:
+        slid, points = slide_row(row)
+        rows.append(slid)
+        gained += points
+    return tuple(rows), gained
+
+
+def _transpose(board: Board) -> Board:
+    """Swap rows and columns."""
+    return tuple(tuple(board[row][column] for row in range(SIZE)) for column in range(SIZE))
+
+
+def _flip_rows(board: Board) -> Board:
+    """Mirror every row left to right."""
+    return tuple(tuple(reversed(row)) for row in board)
--- fold/cli.py ---
hunk 251bece542b0:fold/cli.py#1 (new lines 1..86)
@@ -0,0 +1,86 @@
+"""
+Start Fold and print the one URL a user needs.
+
+Standard library only, no environment variables and no prompts. The game is in memory:
+stopping the process ends the session, and the next start deals a fresh grid.
+
+PRINCIPLE-011.
+"""
+
+import argparse
+import random
+import sys
+import webbrowser
+from typing import List, Optional
+
+from fold.game import Game
+from fold.server import build_server
+
+DEFAULT_PORT = 8766
+
+
+class TriadParser(argparse.ArgumentParser):
+    """Argparse that adds AIKit's Why/Fix triad to a bad flag (PRINCIPLE-011 R5)."""
+
+    def error(self, message: str) -> None:
+        """Print usage and a triad, then exit 2 without opening a socket."""
+        self.print_usage(sys.stderr)
+        self.exit(2, f"{self.prog}: error: {message}\n"
+                     "Why: the flags describe how Fold should start, so a bad value is "
+                     "refused before a socket opens.\n"
+                     "Fix: use --port 1-65535, --host 127.0.0.1, and a whole-number --seed; "
+                     "--help lists them.\n")
+
+
+def port_number(text: str) -> int:
+    """Argparse type for a TCP port, with a message a person can act on."""
+    try:
+        port = int(text)
+    except ValueError as error:
+        raise argparse.ArgumentTypeError("port must be a whole number") from error
+    if not 1 <= port <= 65535:
+        raise argparse.ArgumentTypeError("port must be between 1 and 65535")
+    return port
+
+
+def parse_args(argv: List[str]) -> argparse.Namespace:
+    """The command line: local host, port, optional seed and optional browser open."""
+    parser = TriadParser(
+        prog="python run.py", description="Run Fold, a local tile-merge game.")
+    parser.add_argument("--port", type=port_number, default=DEFAULT_PORT,
+                        help=f"port to listen on (default: {DEFAULT_PORT})")
+    parser.add_argument("--host", default="127.0.0.1",
+                        help="interface to bind (default: 127.0.0.1)")
+    parser.add_argument("--seed", type=int, default=None,
+                        help="make the initial board reproducible")
+    parser.add_argument("--open", action="store_true",
+                        help="open the page in the default browser after starting")
+    return parser.parse_args(argv)
+
+
+def main(argv: Optional[List[str]] = None) -> int:
+    """Serve until interrupted; 0 on a clean stop, 1 on a bind failure, 2 on bad flags."""
+    args = parse_args(sys.argv[1:] if argv is None else argv)
+    game = Game(random.Random(args.seed) if args.seed is not None else None)
+    try:
+        server = build_server(game, args.port, host=args.host)
+    except OSError as error:
+        print(f"could not listen on {args.host}:{args.port}: {error}", file=sys.stderr)
+        print("Why: another process already holds that port, or the interface is unavailable.",
+              file=sys.stderr)
+        print("Fix: stop it, or start Fold with --port <other> and --host 127.0.0.1.",
+              file=sys.stderr)
+        return 1
+    host, port = server.server_address[0], server.server_address[1]
+    display_host = "127.0.0.1" if host in ("0.0.0.0", "::") else host
+    url = f"http://{display_host}:{port}"
+    print(f"Fold is running at {url}  (Ctrl+C to stop)")
+    if args.open:
+        webbrowser.open_new_tab(url)
+    try:
+        server.serve_forever(poll_interval=0.2)
+    except KeyboardInterrupt:
+        print("\nFold stopped.")
+    finally:
+        server.server_close()
+    return 0
--- fold/game.py ---
hunk 251bece542b0:fold/game.py#1 (new lines 1..84)
@@ -0,0 +1,84 @@
+"""
+One game in memory: a board, a score, and a short undo trail.
+
+The server owns exactly one `Game` and serializes every call to it. Keeping the state
+here rather than in the browser means a reload cannot show a board the rules would
+reject, and every transition is exercised by the unit tests without a socket.
+
+PRINCIPLE-003, PRINCIPLE-009, PRINCIPLE-013, PRINCIPLE-014.
+"""
+
+import random
+from typing import Dict, List, Optional, Tuple
+
+from fold.board import Board, empty_board, has_moves, has_won, move as slide, spawn
+
+HISTORY_LIMIT = 20
+
+
+class Game:
+    """A tile-merge game with one-level-or-more undo and a JSON-ready read model."""
+
+    def __init__(self, rng: Optional[random.Random] = None,
+                 board: Optional[Board] = None) -> None:
+        self._rng = rng or random.Random()
+        self._board = board if board is not None else self._starting_board()
+        self._score = 0
+        self._history: List[Tuple[Board, int]] = []
+        self._moves = 0
+
+    def reset(self) -> Dict[str, object]:
+        """Start a fresh game with two tiles and no undo history."""
+        self._board = self._starting_board()
+        self._score = 0
+        self._history = []
+        self._moves = 0
+        return self.state()
+
+    def move(self, direction: str) -> Dict[str, object]:
+        """
+        Apply one direction, spawn one tile after a real move, and report the outcome.
+
+        A blocked direction changes nothing and does not spawn or charge a move.
+        """
+        after, gained = slide(self._board, direction)
+        moved = after != self._board
+        if not moved:
+            return self.state(moved=False, gained=0)
+        self._remember()
+        self._board = spawn(after, self._rng)
+        self._score += gained
+        self._moves += 1
+        return self.state(moved=True, gained=gained)
+
+    def undo(self) -> Dict[str, object]:
+        """Restore the board and score before the last real move, if there is one."""
+        if not self._history:
+            return self.state()
+        self._board, self._score = self._history.pop()
+        self._moves = max(0, self._moves - 1)
+        return self.state()
+
+    def state(self, moved: Optional[bool] = None,
+              gained: int = 0) -> Dict[str, object]:
+        """The flat read model the HTTP layer and the browser both consume."""
+        return {
+            "board": [list(row) for row in self._board],
+            "score": self._score,
+            "won": has_won(self._board),
+            "over": not has_moves(self._board),
+            "canUndo": bool(self._history),
+            "moves": self._moves,
+            "moved": moved,
+            "gained": gained,
+        }
+
+    def _starting_board(self) -> Board:
+        """Two tiles placed by the game's own random source."""
+        return spawn(spawn(empty_board(), self._rng), self._rng)
+
+    def _remember(self) -> None:
+        """Keep the pre-move state for undo, bounded so a long game cannot grow forever."""
+        self._history.append((self._board, self._score))
+        if len(self._history) > HISTORY_LIMIT:
+            self._history.pop(0)
--- fold/server.py ---
hunk 251bece542b0:fold/server.py#1 (new lines 1..168)
@@ -0,0 +1,168 @@
+"""
+The local HTTP layer: static files from `web/` and four JSON endpoints.
+
+The handler only translates requests into `Game` calls. The game rules, scoring and undo
+trail live in `fold.game`, so they are tested without a socket. Every game mutation runs
+under one lock because the server is threaded; a request may render while another moves.
+
+PRINCIPLE-009, PRINCIPLE-010, PRINCIPLE-011, PRINCIPLE-013.
+"""
+
+import json
+import threading
+from dataclasses import dataclass
+from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
+from pathlib import Path
+from typing import Dict, Optional, Tuple
+from urllib.parse import unquote, urlparse
+
+from fold.game import Game
+
+MAX_BODY_BYTES = 4096
+READ_TIMEOUT_SECONDS = 10
+CONTENT_TYPES = {
+    ".html": "text/html; charset=utf-8",
+    ".css": "text/css; charset=utf-8",
+    ".js": "text/javascript; charset=utf-8",
+    ".svg": "image/svg+xml",
+}
+WEB_ROOT = Path(__file__).resolve().parent.parent / "web"
+POST_ROUTES = ("/api/new", "/api/move", "/api/undo")
+
+
+@dataclass(frozen=True)
+class StaticFiles:
+    """Resolves a URL path to a file inside one directory, and never outside it."""
+
+    root: Path
+
+    def resolve(self, url_path: str) -> Optional[Path]:
+        """The file a decoded URL path names, or None when it escapes or does not exist."""
+        relative = unquote(url_path).lstrip("/") or "index.html"
+        candidate = (self.root / relative).resolve()
+        try:
+            candidate.relative_to(self.root.resolve())
+        except ValueError:
+            return None
+        return candidate if candidate.is_file() else None
+
+
+class FoldHandler(BaseHTTPRequestHandler):
+    """Translates requests into `Game` reads and mutations."""
+
+    protocol_version = "HTTP/1.1"
+    server_version = "fold/1.0"
+    sys_version = ""
+    timeout = READ_TIMEOUT_SECONDS
+    disable_nagle_algorithm = True
+    wbufsize = 64 * 1024
+    game: Game
+    lock: threading.Lock
+    files: StaticFiles
+
+    def do_GET(self) -> None:  # noqa: N802 - stdlib handler contract
+        route = unquote(urlparse(self.path).path)
+        if route == "/api/state":
+            with self.lock:
+                payload = self.game.state()
+            self._json(200, payload)
+            return
+        target = self.files.resolve(route)
+        if target is None:
+            self._json(404, {"error": "not found", "path": route})
+            return
+        body = target.read_bytes()
+        self._respond(200, CONTENT_TYPES.get(target.suffix, "application/octet-stream"),
+                      body, cache=route != "/" and not route.endswith(".html"))
+
+    def do_POST(self) -> None:  # noqa: N802 - stdlib handler contract
+        route = unquote(urlparse(self.path).path)
+        if route not in POST_ROUTES:
+            self._json(404, {"error": "not found", "path": route})
+            return
+        try:
+            length = int(self.headers.get("Content-Length") or 0)
+        except ValueError:
+            self._json(400, {"error": "Content-Length must be an integer"})
+            return
+        if length < 0:
+            self._json(400, {"error": "Content-Length must not be negative"})
+            return
+        if length > MAX_BODY_BYTES:
+            self.close_connection = True
+            self._json(413, {"error": f"body over {MAX_BODY_BYTES} bytes"})
+            return
+        raw = self.rfile.read(length) if length else b"{}"
+        try:
+            payload = self._payload(raw)
+            with self.lock:
+                result = self._act(route, payload)
+        except ValueError as error:
+            self._json(400, {"error": str(error)})
+            return
+        self._json(200, result)
+
+    def _payload(self, raw: bytes) -> Dict[str, object]:
+        """Decode one JSON object; anything else is a 400, never a traceback."""
+        try:
+            payload = json.loads(raw.decode("utf-8"))
+        except (UnicodeDecodeError, ValueError) as error:
+            raise ValueError(f"body is not valid JSON: {error}") from error
+        if not isinstance(payload, dict):
+            raise ValueError("body must be a JSON object")
+        return payload
+
+    def _act(self, route: str, payload: Dict[str, object]) -> Dict[str, object]:
+        """Apply one named endpoint to the game and return its read model."""
+        if route == "/api/new":
+            return self.game.reset()
+        if route == "/api/undo":
+            return self.game.undo()
+        direction = payload.get("direction")
+        if not isinstance(direction, str):
+            raise ValueError("body needs a string 'direction'")
+        return self.game.move(direction)
+
+    def _json(self, status: int, payload: Dict[str, object]) -> None:
+        body = json.dumps(payload).encode("utf-8")
+        self._respond(status, "application/json; charset=utf-8", body, cache=False)
+
+    def _respond(self, status: int, content_type: str, body: bytes, cache: bool) -> None:
+        self.send_response(status)
+        self.send_header("Content-Type", content_type)
+        self.send_header("Content-Length", str(len(body)))
+        self.send_header("Cache-Control", "max-age=60" if cache else "no-store")
+        self.end_headers()
+        self.wfile.write(body)
+        self.wfile.flush()
+
+    def end_headers(self) -> None:
+        """Attach the security policy to every response, including stdlib errors."""
+        self.send_header("Content-Security-Policy",
+                         "default-src 'self'; img-src 'self' data:; style-src 'self'; "
+                         "script-src 'self'; connect-src 'self'; base-uri 'none'; "
+                         "form-action 'self'; frame-ancestors 'none'")
+        self.send_header("X-Content-Type-Options", "nosniff")
+        self.send_header("Referrer-Policy", "no-referrer")
+        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
+        super().end_headers()
+
+    def log_message(self, format: str, *args) -> None:
+        """Silent by default; `fold.cli` prints the one line a user needs."""
+
+
+class FoldHTTPServer(ThreadingHTTPServer):
+    """A local thread-per-request server whose threads do not outlive the process."""
+
+    daemon_threads = True
+
+
+def build_server(game: Game, port: int, web: Path = WEB_ROOT,
+                 host: str = "127.0.0.1") -> FoldHTTPServer:
+    """An HTTP server bound to `host:port`, serving `web` and one in-memory game."""
+    handler = type("BoundFoldHandler", (FoldHandler,), {
+        "game": game,
+        "lock": threading.Lock(),
+        "files": StaticFiles(web),
+    })
+    return FoldHTTPServer((host, port), handler)
--- play.bat ---
hunk 251bece542b0:play.bat#1 (new lines 1..18)
@@ -0,0 +1,18 @@
+@echo off
+setlocal EnableExtensions
+title Fold
+cd /d "%~dp0"
+
+set "PYTHON_CMD=python"
+where py >nul 2>&1
+if not errorlevel 1 (
+    py -3 -c "import sys" >nul 2>&1
+    if not errorlevel 1 set "PYTHON_CMD=py -3"
+)
+
+%PYTHON_CMD% run.py --open %*
+if errorlevel 1 (
+    echo.
+    echo Fold stopped with an error. The message above says why.
+    pause
+)
--- play.command ---
hunk 251bece542b0:play.command#1 (new lines 1..5)
@@ -0,0 +1,5 @@
+#!/bin/sh
+# macOS double-click launcher: run the POSIX launcher beside this file.
+set -eu
+cd "$(dirname "$0")"
+exec sh ./play.sh "$@"
--- play.sh ---
hunk 251bece542b0:play.sh#1 (new lines 1..5)
@@ -0,0 +1,5 @@
+#!/bin/sh
+# One-click launcher for macOS and Linux: start Fold and open its page.
+set -eu
+cd "$(dirname "$0")"
+exec python3 run.py --open "$@"
--- pyproject.toml ---
hunk 251bece542b0:pyproject.toml#1 (new lines 1..6)
@@ -0,0 +1,6 @@
+[project]
+name = "fold"
+version = "1.0.0"
+description = "A small 4x4 tile-merge game with a local browser surface."
+requires-python = ">=3.9"
+dependencies = []
--- run.py ---
hunk 251bece542b0:run.py#1 (new lines 1..9)
@@ -0,0 +1,9 @@
+#!/usr/bin/env python3
+"""The user-facing entry point: `python run.py` starts Fold on port 8766."""
+
+import sys
+
+from fold.cli import main
+
+if __name__ == "__main__":
+    sys.exit(main())
--- start.bat ---
hunk 251bece542b0:start.bat#1 (new lines 1..4)
@@ -0,0 +1,4 @@
+@echo off
+setlocal
+call "%~dp0play.bat" %*
+exit /b %ERRORLEVEL%
--- start.command ---
hunk 251bece542b0:start.command#1 (new lines 1..5)
@@ -0,0 +1,5 @@
+#!/bin/sh
+# macOS double-click alias for play.command.
+set -eu
+cd "$(dirname "$0")"
+exec sh ./play.sh "$@"
--- start.sh ---
hunk 251bece542b0:start.sh#1 (new lines 1..5)
@@ -0,0 +1,5 @@
+#!/bin/sh
+# Alias for play.sh: start Fold and open its page.
+set -eu
+cd "$(dirname "$0")"
+exec sh ./play.sh "$@"
--- tests/__init__.py ---
hunk 251bece542b0:tests/__init__.py#1 (new lines 1..1)
@@ -0,0 +1 @@
+"""Fold's test package."""
--- tests/test_board.py ---
hunk 251bece542b0:tests/test_board.py#1 (new lines 1..85)
@@ -0,0 +1,85 @@
+"""Pure board rules: sliding, merging, spawning and terminal detection."""
+
+import random
+import unittest
+
+from fold.board import (empty_board, has_moves, has_won, move, slide_row, spawn)
+
+
+class SlideRowTest(unittest.TestCase):
+
+    def test_equal_neighbours_merge_once_and_earn_their_sum(self):
+        self.assertEqual(((4, 4, 0, 0), 8), slide_row((2, 2, 2, 2)))
+
+    def test_zeros_compact_before_merging(self):
+        self.assertEqual(((4, 0, 0, 0), 4), slide_row((0, 2, 0, 2)))
+
+    def test_a_merged_tile_never_merges_again_in_the_same_slide(self):
+        self.assertEqual(((8, 8, 0, 0), 8), slide_row((4, 4, 8, 0)))
+
+    def test_a_row_with_no_pair_only_compacts(self):
+        self.assertEqual(((2, 4, 8, 0), 0), slide_row((0, 2, 4, 8)))
+
+
+class MoveTest(unittest.TestCase):
+
+    def test_left_and_right_are_mirror_images(self):
+        board = ((2, 0, 2, 4), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+        left, left_points = move(board, "left")
+        right, right_points = move(board, "right")
+        self.assertEqual(((4, 4, 0, 0),) + ((0, 0, 0, 0),) * 3, left)
+        self.assertEqual(((0, 0, 4, 4),) + ((0, 0, 0, 0),) * 3, right)
+        self.assertEqual((left_points, right_points), (4, 4))
+
+    def test_up_and_down_are_mirror_images(self):
+        board = ((2, 0, 0, 0), (2, 0, 0, 0), (4, 0, 0, 0), (0, 0, 0, 0))
+        up, up_points = move(board, "up")
+        down, down_points = move(board, "down")
+        self.assertEqual(((4, 0, 0, 0), (4, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)), up)
+        self.assertEqual(((0, 0, 0, 0), (0, 0, 0, 0), (4, 0, 0, 0), (4, 0, 0, 0)), down)
+        self.assertEqual((up_points, down_points), (4, 4))
+
+    def test_an_unknown_direction_is_refused(self):
+        with self.assertRaisesRegex(ValueError, "direction must be one of"):
+            move(empty_board(), "sideways")
+
+
+class SpawnTest(unittest.TestCase):
+
+    def test_spawn_places_the_requested_number_of_tiles_in_empty_cells(self):
+        board = spawn(empty_board(), random.Random(3), count=2)
+        values = [value for row in board for value in row]
+        self.assertEqual(2, sum(1 for value in values if value))
+        self.assertTrue(all(value in (0, 2, 4) for value in values))
+
+    def test_spawn_with_a_shared_seed_is_replayable(self):
+        first = spawn(empty_board(), random.Random(11), count=3)
+        second = spawn(empty_board(), random.Random(11), count=3)
+        self.assertEqual(first, second)
+
+    def test_spawn_never_overwrites_a_tile(self):
+        full = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
+        self.assertEqual(full, spawn(full, random.Random(1), count=4))
+
+
+class TerminalTest(unittest.TestCase):
+
+    def test_winning_value_is_detected(self):
+        board = ((2048, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+        self.assertTrue(has_won(board))
+        self.assertFalse(has_won(empty_board()))
+
+    def test_an_empty_cell_leaves_a_move(self):
+        self.assertTrue(has_moves(empty_board()))
+
+    def test_a_full_checkerboard_has_no_moves(self):
+        board = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
+        self.assertFalse(has_moves(board))
+
+    def test_a_full_board_with_an_equal_neighbour_still_moves(self):
+        board = ((2, 2, 4, 8), (4, 8, 16, 32), (2, 4, 8, 16), (4, 8, 16, 32))
+        self.assertTrue(has_moves(board))
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tests/test_cli.py ---
hunk 251bece542b0:tests/test_cli.py#1 (new lines 1..44)
@@ -0,0 +1,44 @@
+"""Command-line parsing: local defaults, an optional seed and a validated port."""
+
+import argparse
+import contextlib
+import io
+import unittest
+
+from fold.cli import parse_args, port_number
+
+
+class CliTest(unittest.TestCase):
+
+    def test_defaults_keep_the_game_local(self):
+        args = parse_args([])
+        self.assertEqual(8766, args.port)
+        self.assertEqual("127.0.0.1", args.host)
+        self.assertIsNone(args.seed)
+        self.assertFalse(args.open)
+
+    def test_a_seed_and_open_are_opt_in(self):
+        args = parse_args(["--seed", "7", "--open"])
+        self.assertEqual(7, args.seed)
+        self.assertTrue(args.open)
+
+    def test_a_port_outside_the_valid_range_is_refused(self):
+        for value in ("0", "65536", "http"):
+            with self.assertRaises(argparse.ArgumentTypeError):
+                port_number(value)
+
+    def test_a_valid_port_is_an_integer(self):
+        self.assertEqual(8080, port_number("8080"))
+
+    def test_a_bad_flag_exits_two_with_a_triad(self):
+        stderr = io.StringIO()
+        with self.assertRaises(SystemExit) as caught:
+            with contextlib.redirect_stderr(stderr):
+                parse_args(["--port", "0"])
+        self.assertEqual(2, caught.exception.code)
+        self.assertIn("Why:", stderr.getvalue())
+        self.assertIn("Fix:", stderr.getvalue())
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tests/test_game.py ---
hunk 251bece542b0:tests/test_game.py#1 (new lines 1..82)
@@ -0,0 +1,82 @@
+"""One game's state transitions: start, move, undo and terminal read model."""
+
+import random
+import unittest
+
+from fold.board import empty_board
+from fold.game import Game
+
+START = ((2, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+LOCKED = ((2, 4, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+
+
+class GameTest(unittest.TestCase):
+
+    def test_a_new_game_has_two_tiles_and_no_history(self):
+        game = Game(random.Random(5))
+        state = game.state()
+        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
+        self.assertEqual(0, state["score"])
+        self.assertFalse(state["canUndo"])
+        self.assertEqual(0, state["moves"])
+
+    def test_a_move_merges_scores_and_spawns_exactly_one_tile(self):
+        game = Game(random.Random(2), board=START)
+        state = game.move("left")
+        self.assertTrue(state["moved"])
+        self.assertEqual(4, state["score"])
+        self.assertEqual(4, state["gained"])
+        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
+        self.assertEqual(1, state["moves"])
+        self.assertTrue(state["canUndo"])
+
+    def test_a_blocked_direction_changes_nothing(self):
+        game = Game(random.Random(2), board=LOCKED)
+        before = game.state()
+        after = game.move("left")
+        self.assertFalse(after["moved"])
+        self.assertEqual(before["board"], after["board"])
+        self.assertEqual(0, after["score"])
+        self.assertEqual(0, after["moves"])
+        self.assertFalse(after["canUndo"])
+
+    def test_undo_restores_the_board_and_score(self):
+        game = Game(random.Random(2), board=START)
+        before = game.state()
+        game.move("left")
+        restored = game.undo()
+        self.assertEqual(before["board"], restored["board"])
+        self.assertEqual(before["score"], restored["score"])
+        self.assertFalse(restored["canUndo"])
+
+    def test_reset_deals_a_new_board_and_clears_history(self):
+        game = Game(random.Random(2), board=START)
+        game.move("left")
+        state = game.reset()
+        self.assertEqual(0, state["score"])
+        self.assertEqual(0, state["moves"])
+        self.assertFalse(state["canUndo"])
+        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
+
+    def test_a_full_checkerboard_reports_game_over(self):
+        board = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
+        state = Game(random.Random(1), board=board).state()
+        self.assertTrue(state["over"])
+        self.assertFalse(state["won"])
+
+    def test_a_2048_tile_reports_a_win(self):
+        board = ((2048, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+        state = Game(random.Random(1), board=board).state()
+        self.assertTrue(state["won"])
+        self.assertFalse(state["over"])
+
+    def test_state_has_the_declared_json_shape(self):
+        state = Game(random.Random(1), board=empty_board()).state(moved=True, gained=8)
+        self.assertEqual({"board", "score", "won", "over", "canUndo", "moves", "moved", "gained"},
+                         set(state))
+        self.assertTrue(state["moved"])
+        self.assertEqual(8, state["gained"])
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tests/test_inventory.py ---
hunk 251bece542b0:tests/test_inventory.py#1 (new lines 1..29)
@@ -0,0 +1,29 @@
+"""The UI inventory proof covers the controls, handlers, live region and theme tokens."""
+
+import unittest
+from pathlib import Path
+
+from tools.ui_inventory import inventory
+
+WEB = Path(__file__).resolve().parent.parent / "web"
+
+
+class InventoryTest(unittest.TestCase):
+
+    def test_the_inventory_names_the_controls_and_theme_tokens(self):
+        entries = inventory(WEB)
+        for expected in ("element div#board", "action new", "handler undo",
+                         "live-region status", "token --tile-2048-bg"):
+            self.assertIn(expected, entries)
+        self.assertGreaterEqual(len(entries), 60)
+
+    def test_the_page_and_script_are_part_of_the_surface(self):
+        entries = inventory(WEB)
+        self.assertIn("element output#score", entries)
+        self.assertIn("element output#moves", entries)
+        self.assertIn("element button#new-game", entries)
+        self.assertIn("handler continue", entries)
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tests/test_launchers.py ---
hunk 251bece542b0:tests/test_launchers.py#1 (new lines 1..45)
@@ -0,0 +1,45 @@
+"""One-click launch files: present, CRLF-safe on Windows and pointing at run.py."""
+
+import unittest
+from pathlib import Path
+
+ROOT = Path(__file__).resolve().parent.parent
+BATCH = ROOT / "play.bat"
+SHELL = ROOT / "play.sh"
+COMMAND = ROOT / "play.command"
+START_BATCH = ROOT / "start.bat"
+START_SHELL = ROOT / "start.sh"
+START_COMMAND = ROOT / "start.command"
+
+
+class LauncherTest(unittest.TestCase):
+
+    def test_every_launcher_exists(self):
+        for path in (BATCH, SHELL, COMMAND, START_BATCH, START_SHELL, START_COMMAND):
+            self.assertTrue(path.is_file(), path.name)
+
+    def test_batch_files_have_crlf_line_endings(self):
+        for path in (BATCH, START_BATCH):
+            data = path.read_bytes()
+            self.assertEqual(0, data.replace(b"\r\n", b"").count(b"\n"),
+                             f"{path.name} must use CRLF so cmd.exe parses it reliably")
+
+    def test_launchers_start_the_game_and_aliases_delegate(self):
+        self.assertIn("run.py --open", BATCH.read_text(encoding="utf-8"))
+        self.assertIn("run.py --open", SHELL.read_text(encoding="utf-8"))
+        self.assertIn("sh ./play.sh", COMMAND.read_text(encoding="utf-8"))
+        self.assertIn("play.bat", START_BATCH.read_text(encoding="utf-8"))
+        self.assertIn("play.sh", START_SHELL.read_text(encoding="utf-8"))
+        self.assertIn("play.sh", START_COMMAND.read_text(encoding="utf-8"))
+
+    def test_a_batch_failure_stays_visible(self):
+        self.assertIn("pause", BATCH.read_text(encoding="utf-8").lower())
+
+    def test_gitattributes_pins_launcher_line_endings(self):
+        attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
+        self.assertIn("*.bat text eol=crlf", attributes)
+        self.assertIn("*.sh text eol=lf", attributes)
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tests/test_server.py ---
hunk 251bece542b0:tests/test_server.py#1 (new lines 1..138)
@@ -0,0 +1,138 @@
+"""The HTTP layer over a real socket: JSON endpoints, static files and hostile input."""
+
+import json
+import random
+import tempfile
+import threading
+import unittest
+import urllib.error
+import urllib.request
+from pathlib import Path
+from typing import Optional, Tuple
+
+from fold.game import Game
+from fold.server import StaticFiles, build_server
+
+START = ((2, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
+
+
+class ServerHarness:
+    """One server on an ephemeral port, torn down without a lingering thread."""
+
+    def __init__(self, board=START) -> None:
+        self.game = Game(random.Random(4), board=board)
+        self.server = build_server(self.game, 0)
+        self.thread = threading.Thread(target=self.server.serve_forever,
+                                       kwargs={"poll_interval": 0.01}, daemon=True)
+        self.thread.start()
+        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
+
+    def close(self) -> None:
+        self.server.shutdown()
+        self.server.server_close()
+        self.thread.join(2)
+
+    def request(self, path: str, payload: Optional[bytes] = None) -> Tuple[int, bytes]:
+        request = urllib.request.Request(self.base + path, data=payload, method="POST" if payload is not None else "GET")
+        if payload is not None:
+            request.add_header("Content-Type", "application/json")
+        try:
+            with urllib.request.urlopen(request, timeout=5) as response:
+                return response.status, response.read()
+        except urllib.error.HTTPError as error:
+            with error:
+                return error.code, error.read()
+
+
+class ServerTest(unittest.TestCase):
+
+    def setUp(self):
+        self.harness = ServerHarness()
+        self.addCleanup(self.harness.close)
+
+    def test_the_page_and_assets_are_served(self):
+        for path, marker in (("/", b'id="board"'), ("/theme.css", b"--paper"),
+                             ("/app.css", b".board"), ("/app.js", b"ACTIONS"),
+                             ("/favicon.svg", b"<svg")):
+            status, body = self.harness.request(path)
+            self.assertEqual(200, status, path)
+            self.assertIn(marker, body, path)
+
+    def test_security_headers_are_present(self):
+        with urllib.request.urlopen(self.harness.base + "/", timeout=5) as response:
+            headers = response.headers
+        self.assertEqual("nosniff", headers.get("X-Content-Type-Options"))
+        self.assertEqual("no-referrer", headers.get("Referrer-Policy"))
+        self.assertEqual("same-origin", headers.get("Cross-Origin-Resource-Policy"))
+        self.assertIn("default-src 'self'", headers.get("Content-Security-Policy", ""))
+        self.assertTrue((headers.get("Server") or "").startswith("fold/"))
+
+    def test_state_returns_the_declared_shape(self):
+        status, body = self.harness.request("/api/state")
+        state = json.loads(body)
+        self.assertEqual(200, status)
+        self.assertEqual({"board", "score", "won", "over", "canUndo", "moves", "moved", "gained"},
+                         set(state))
+
+    def test_a_move_merges_and_spawns_a_tile(self):
+        status, body = self.harness.request("/api/move", b'{"direction":"left"}')
+        state = json.loads(body)
+        self.assertEqual(200, status)
+        self.assertTrue(state["moved"])
+        self.assertEqual(4, state["score"])
+        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
+
+    def test_undo_restores_the_previous_board(self):
+        before = json.loads(self.harness.request("/api/state")[1])
+        self.harness.request("/api/move", b'{"direction":"left"}')
+        after = json.loads(self.harness.request("/api/undo", b"{}")[1])
+        self.assertEqual(before["board"], after["board"])
+        self.assertEqual(before["score"], after["score"])
+        self.assertFalse(after["canUndo"])
+
+    def test_a_bad_direction_is_a_400_with_an_error(self):
+        status, body = self.harness.request("/api/move", b'{"direction":"diagonal"}')
+        self.assertEqual(400, status)
+        self.assertIn("direction must be one of", json.loads(body)["error"])
+
+    def test_malformed_json_is_a_400(self):
+        status, body = self.harness.request("/api/move", b"{not json")
+        self.assertEqual(400, status)
+        self.assertIn("not valid JSON", json.loads(body)["error"])
+
+    def test_an_oversized_body_is_a_413(self):
+        status, _ = self.harness.request("/api/move", b"{" + b"x" * 5000 + b"}")
+        self.assertEqual(413, status)
+
+    def test_an_unknown_route_is_a_json_404(self):
+        status, body = self.harness.request("/api/missing")
+        self.assertEqual(404, status)
+        self.assertEqual("not found", json.loads(body)["error"])
+
+    def test_a_trailing_slash_is_not_the_index(self):
+        status, _ = self.harness.request("/missing/")
+        self.assertEqual(404, status)
+
+
+class StaticFilesTest(unittest.TestCase):
+
+    def setUp(self):
+        directory = tempfile.TemporaryDirectory()
+        self.addCleanup(directory.cleanup)
+        self.root = Path(directory.name)
+        (self.root / "web").mkdir()
+        (self.root / "web" / "index.html").write_text("<p>hi</p>", encoding="utf-8")
+        (self.root / "secret.txt").write_text("nope", encoding="utf-8")
+        self.files = StaticFiles(self.root / "web")
+
+    def test_root_serves_the_index(self):
+        self.assertEqual("index.html", self.files.resolve("/").name)
+
+    def test_paths_outside_the_web_root_are_refused(self):
+        self.assertIsNone(self.files.resolve("/../secret.txt"))
+        self.assertIsNone(self.files.resolve("/%2e%2e/secret.txt"))
+        self.assertIsNone(self.files.resolve("/missing.css"))
+
+
+if __name__ == "__main__":
+    unittest.main()
--- tools/__init__.py ---
hunk 251bece542b0:tools/__init__.py#1 (new lines 1..1)
@@ -0,0 +1 @@
+"""Developer proofs for Fold."""
--- tools/dogfood.py ---
hunk 251bece542b0:tools/dogfood.py#1 (new lines 1..278)
@@ -0,0 +1,278 @@
+#!/usr/bin/env python3
+"""
+Fold's dogfood runner: play it the way a user does, then attack the surface.
+
+The golden path starts a real server on a free port, loads the page, starts a game,
+makes a real move, undoes it and reads the state back. The chaos track sends malformed
+JSON, bad directions, oversized bodies, concurrent reads, traversal attempts and unknown
+routes. Every process runs inside a context manager that kills its whole tree, the run
+uses one temporary sandbox and the tracked tree is fingerprinted before and after.
+
+Usage: python tools/dogfood.py   (exit 0 pass, 1 fail, 2 cannot run)
+
+PRINCIPLE-015.
+"""
+
+import contextlib
+import hashlib
+import json
+import os
+import signal
+import socket
+import subprocess
+import sys
+import tempfile
+import threading
+import time
+import urllib.error
+import urllib.request
+from pathlib import Path
+from typing import Dict, List, Optional, Tuple
+
+ROOT = Path(__file__).resolve().parent.parent
+LOG_PATH = ROOT / ".aikit" / "dogfood_last_run.log"
+MAX_REPORT_LINES = 15
+START_TIMEOUT = 20.0
+REQUEST_TIMEOUT = 5.0
+SUBPROCESS_TIMEOUT = 30
+STATE_FIELDS = ("board", "score", "won", "over", "canUndo", "moves", "moved", "gained")
+CONTROLS = (b'id="board"', b'id="new-game"', b'id="undo"', b'id="status"',
+            b'data-action="new"', b'data-action="undo"')
+DIRECTIONS = ("left", "up", "right", "down")
+
+
+class Report:
+    """Collects step outcomes: the console sees a summary, the log sees everything."""
+
+    def __init__(self) -> None:
+        self.lines: List[str] = []
+        self.failures: List[str] = []
+
+    def step(self, ok: bool, label: str, detail: str = "") -> bool:
+        """Record one step's outcome and hand back whether it passed."""
+        mark = "PASS" if ok else "FAIL"
+        self.lines.append(f"[{mark}] {label}" + (f" :: {detail}" if detail else ""))
+        if not ok:
+            self.failures.append(f"{label}: {detail}" if detail else label)
+        return ok
+
+
+def terminate_process_tree(process: subprocess.Popen) -> None:
+    """Kill a process and everything it started, on Windows and POSIX alike."""
+    if process.poll() is not None:
+        return
+    try:
+        if os.name == "nt":
+            subprocess.run(["taskkill", "/F", "/T", "/PID", str(process.pid)],
+                           capture_output=True, timeout=SUBPROCESS_TIMEOUT)
+        else:
+            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
+    except (OSError, subprocess.SubprocessError):
+        process.kill()
+    with contextlib.suppress(subprocess.TimeoutExpired):
+        process.wait(timeout=10)
+
+
+@contextlib.contextmanager
+def supervised(command: List[str], log):
+    """Run a command with stdin closed, killing its whole tree on the way out."""
+    if os.name == "nt":
+        creation = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
+    else:
+        creation = {"start_new_session": True}
+    options = dict(stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
+                   cwd=str(ROOT), **creation)
+    process = subprocess.Popen(command, **options)  # hygiene: allow RAII teardown
+    try:
+        yield process
+    finally:
+        terminate_process_tree(process)
+
+
+def free_port() -> int:
+    """A port the operating system says is free right now."""
+    with socket.socket() as probe:
+        probe.bind(("127.0.0.1", 0))
+        return int(probe.getsockname()[1])
+
+
+def fingerprint() -> str:
+    """A digest of every tracked file, so a run that dirties the repository fails."""
+    listing = subprocess.run(["git", "ls-files", "-z"], cwd=str(ROOT), capture_output=True,
+                             timeout=SUBPROCESS_TIMEOUT)
+    digest = hashlib.sha256()
+    for name in sorted(part for part in listing.stdout.split(b"\0") if part):
+        digest.update(name)
+        path = ROOT / name.decode("utf-8")
+        if path.is_file():
+            digest.update(path.read_bytes())
+    return digest.hexdigest()
+
+
+def get(base: str, path: str) -> Tuple[int, bytes, float]:
+    """One GET, with the milliseconds it took."""
+    started = time.monotonic()
+    try:
+        with urllib.request.urlopen(base + path, timeout=REQUEST_TIMEOUT) as response:
+            body = response.read()
+            status = response.status
+    except urllib.error.HTTPError as error:
+        with error:
+            return error.code, error.read(), (time.monotonic() - started) * 1000.0
+    return status, body, (time.monotonic() - started) * 1000.0
+
+
+def post(base: str, path: str, payload: object, raw: Optional[bytes] = None) -> Tuple[int, bytes]:
+    """One POST; an HTTP error is an answer here, not an exception."""
+    data = raw if raw is not None else json.dumps(payload).encode("utf-8")
+    request = urllib.request.Request(base + path, data=data, method="POST",
+                                     headers={"Content-Type": "application/json"})
+    try:
+        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
+            return response.status, response.read()
+    except urllib.error.HTTPError as error:
+        with error:
+            return error.code, error.read()
+
+
+def wait_until_serving(base: str) -> bool:
+    """True once the server answers, False if it never does within the start timeout."""
+    deadline = time.monotonic() + START_TIMEOUT
+    while time.monotonic() < deadline:
+        try:
+            get(base, "/api/state")
+            return True
+        except (urllib.error.URLError, OSError):
+            time.sleep(0.05)
+    return False
+
+
+def golden_path(base: str, report: Report) -> None:
+    """Load the page, make a move, undo it and read the state back."""
+    status, page, _ = get(base, "/")
+    report.step(status == 200 and all(control in page for control in CONTROLS),
+                "page serves every control the script renders into",
+                f"HTTP {status}, {len(page)} bytes")
+
+    code, body, elapsed = get(base, "/api/state")
+    first = json.loads(body)
+    report.step(code == 200 and all(field in first for field in STATE_FIELDS),
+                "GET /api/state answers the declared schema", f"HTTP {code}")
+    report.step(elapsed < 500.0, "state answers inside its 500ms budget", f"{elapsed:.0f}ms")
+    report.step(sum(1 for row in first["board"] for value in row if value) == 2,
+                "a fresh game starts with two tiles")
+
+    moved = None
+    for direction in DIRECTIONS:
+        code, body = post(base, "/api/move", {"direction": direction})
+        candidate = json.loads(body)
+        if code == 200 and candidate["moved"]:
+            moved = candidate
+            break
+    report.step(moved is not None, "at least one direction moves the opening board")
+
+    if moved is not None:
+        count = sum(1 for row in moved["board"] for value in row if value)
+        report.step(count >= 2 and moved["canUndo"] is True,
+                    "a real move spawns a tile and leaves an undo",
+                    f"{count} tiles, score {moved['score']}")
+        code, body = post(base, "/api/undo", {})
+        restored = json.loads(body)
+        report.step(code == 200 and restored["board"] == first["board"],
+                    "undo restores the opening board", f"HTTP {code}")
+
+
+def chaos(base: str, report: Report) -> None:
+    """Hostile input: malformed JSON, bad directions, a flood and traversal."""
+    code, body = post(base, "/api/move", None, raw=b"{not json at all")
+    report.step(code == 400 and b"error" in body, "malformed JSON answers 400", f"HTTP {code}")
+
+    code, body = post(base, "/api/move", {"direction": "diagonal"})
+    report.step(code == 400 and b"direction must be one of" in body,
+                "a bad direction answers 400", f"HTTP {code}")
+
+    code, _ = post(base, "/api/move", None, raw=b"{" + b"x" * 8192 + b"}")
+    report.step(code == 413, "an oversized body answers 413", f"HTTP {code}")
+
+    code, _ = post(base, "/api/move", [1, 2, 3])
+    report.step(code == 400, "a JSON array body answers 400", f"HTTP {code}")
+
+    results: Dict[int, int] = {}
+    lock = threading.Lock()
+
+    def hammer() -> None:
+        try:
+            status = get(base, "/api/state")[0]
+        except (urllib.error.URLError, OSError):
+            status = 0
+        with lock:
+            results[status] = results.get(status, 0) + 1
+
+    threads = [threading.Thread(target=hammer) for _ in range(12)]
+    for thread in threads:
+        thread.start()
+    for thread in threads:
+        thread.join(REQUEST_TIMEOUT * 2)
+    report.step(results.get(200) == len(threads), "12 concurrent reads all answer 200",
+                str(results))
+
+    code = get(base, "/%2e%2e/README.md")[0]
+    report.step(code == 404, "a traversal attempt answers 404", f"HTTP {code}")
+
+    code, body, _ = get(base, "/api/missing")
+    report.step(code == 404 and b"not found" in body, "an unknown route answers a JSON 404",
+                f"HTTP {code}")
+
+
+def surface_proof(report: Report, log) -> None:
+    """The UI inventory proof runs and reports its surface, as the UI guard expects."""
+    done = subprocess.run([sys.executable, str(ROOT / "tools" / "ui_inventory.py")],
+                          capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT,
+                          cwd=str(ROOT))
+    log.write(done.stdout + done.stderr)
+    entries = [line for line in done.stdout.splitlines() if line.strip()]
+    report.step(done.returncode == 0 and len(entries) >= 20,
+                "the UI inventory proof reports its surface", f"{len(entries)} entries")
+
+
+def main() -> int:
+    """Run both tracks in one sandbox and print at most 15 lines."""
+    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
+    report = Report()
+    before = fingerprint()
+    with tempfile.TemporaryDirectory(prefix="fold-dogfood-") as box:
+        with open(LOG_PATH, "w", encoding="utf-8") as log:
+            port = free_port()
+            base = f"http://127.0.0.1:{port}"
+            command = [sys.executable, str(ROOT / "run.py"), "--port", str(port),
+                       "--seed", "7"]
+            alive = False
+            with supervised(command, log) as process:
+                if wait_until_serving(base):
+                    report.step(True, "the server starts and answers", base)
+                    golden_path(base, report)
+                    chaos(base, report)
+                else:
+                    report.step(False, "the server starts and answers",
+                                f"no answer within {START_TIMEOUT:.0f}s")
+                alive = process.poll() is None
+                log.write(f"\nsandbox={box}\n")
+            report.step(alive, "the server survived every hostile input")
+            surface_proof(report, log)
+            log.write("\n".join(report.lines) + "\n")
+
+    report.step(fingerprint() == before, "the run left the tracked tree untouched")
+    passed = len(report.lines) - len(report.failures)
+    print(f"FOLD DOGFOOD (PRINCIPLE-015): {passed}/{len(report.lines)} steps passed")
+    for failure in report.failures[:MAX_REPORT_LINES - 4]:
+        print(f"  [FAIL] {failure}")
+    print(f"  full log: {LOG_PATH.relative_to(ROOT).as_posix()}")
+    if report.failures:
+        print("Why: the product must work and hold up under hostile input before it ships.")
+        print("Fix: read the log, fix the failing step, then rerun this command.")
+        return 1
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
--- tools/ui_inventory.py ---
hunk 251bece542b0:tools/ui_inventory.py#1 (new lines 1..101)
@@ -0,0 +1,101 @@
+"""
+Print Fold's UI inventory, one entry per line.
+
+The UI guard snapshots this output before a surface edit and compares it afterwards, so
+a dropped control, action, handler or theme token becomes a lost line. The dump is pure
+parsing: it never starts a server or a browser, and its order is stable.
+
+Usage: python tools/ui_inventory.py [web-directory]
+
+PRINCIPLE-003, PRINCIPLE-010, PRINCIPLE-015.
+"""
+
+import re
+import sys
+from html.parser import HTMLParser
+from pathlib import Path
+from typing import List, Set
+
+WEB_DIR = Path(__file__).resolve().parent.parent / "web"
+HANDLER_PATTERN = re.compile(r"^\s*var ACTIONS = \{(?P<body>[^}]*)\}", re.MULTILINE)
+KEY_PATTERN = re.compile(r"(\w+)\s*:")
+TOKEN_PATTERN = re.compile(r"^\s*(--[a-z0-9-]+)\s*:", re.MULTILINE)
+
+
+class SurfaceParser(HTMLParser):
+    """Collects identified elements, named actions and live regions of one page."""
+
+    def __init__(self) -> None:
+        super().__init__(convert_charrefs=True)
+        self.entries: Set[str] = set()
+
+    def handle_starttag(self, tag: str, attrs) -> None:
+        values = {name: value or "" for name, value in attrs}
+        element = values.get("id")
+        if element:
+            self.entries.add(f"element {tag}#{element}")
+        action = values.get("data-action")
+        if action:
+            self.entries.add(f"action {action}")
+        if "aria-live" in values:
+            self.entries.add(f"live-region {values.get('id') or tag}")
+        if values.get("role"):
+            self.entries.add(f"role {values['role']}")
+
+
+def html_entries(path: Path) -> Set[str]:
+    """Identified elements, actions, roles and live regions declared in a page."""
+    parser = SurfaceParser()
+    parser.feed(path.read_text(encoding="utf-8"))
+    parser.close()
+    return parser.entries
+
+
+def handler_entries(path: Path) -> Set[str]:
+    """Action names the browser script is willing to dispatch."""
+    match = HANDLER_PATTERN.search(path.read_text(encoding="utf-8"))
+    if not match:
+        return set()
+    return {f"handler {name}" for name in KEY_PATTERN.findall(match.group("body"))}
+
+
+def token_entries(path: Path) -> Set[str]:
+    """Theme custom properties the stylesheet declares."""
+    text = path.read_text(encoding="utf-8")
+    return {f"token {name}" for name in TOKEN_PATTERN.findall(text)}
+
+
+def inventory(web: Path) -> List[str]:
+    """Every inventory entry of a web directory, sorted and deduplicated."""
+    entries: Set[str] = set()
+    for page in sorted(web.glob("*.html")):
+        entries |= html_entries(page)
+    for script in sorted(web.glob("*.js")):
+        entries |= handler_entries(script)
+    theme = web / "theme.css"
+    if theme.exists():
+        entries |= token_entries(theme)
+    return sorted(entries)
+
+
+def main(argv: List[str]) -> int:
+    """Write the inventory to stdout; exit 1 when the surface has no entries at all."""
+    web = Path(argv[1]).resolve() if len(argv) > 1 else WEB_DIR
+    if not web.is_dir():
+        print(f"no such web directory: {web}", file=sys.stderr)
+        print("Why: the inventory proof needs Fold's web/ surface.", file=sys.stderr)
+        print("Fix: run it from the project root, or pass the directory.", file=sys.stderr)
+        return 2
+    entries = inventory(web)
+    if not entries:
+        print(f"no UI inventory found under {web}", file=sys.stderr)
+        print("Why: an empty inventory would hide every lost control.", file=sys.stderr)
+        print("Fix: check that web/index.html still carries ids and data-action buttons.",
+              file=sys.stderr)
+        return 1
+    print("\n".join(entries))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv))
--- web/app.css ---
hunk 251bece542b0:web/app.css#1 (new lines 1..382)
@@ -0,0 +1,382 @@
+/* Layout and motion for Fold. Every colour and type value comes from theme.css. */
+
+* {
+  box-sizing: border-box;
+}
+
+html {
+  min-height: 100%;
+}
+
+body {
+  margin: 0;
+  min-height: 100vh;
+  color: var(--ink);
+  background-color: var(--paper);
+  background-image:
+    radial-gradient(circle at 12% -8%, var(--glow-a), transparent 42%),
+    radial-gradient(circle at 92% 8%, var(--glow-b), transparent 38%);
+  font-family: var(--font-sans);
+  font-size: var(--text-md);
+  font-weight: var(--weight-regular);
+  line-height: 1.5;
+}
+
+.page {
+  width: min(100%, 1040px);
+  margin: 0 auto;
+  padding: clamp(20px, 4.5vw, 56px);
+  display: grid;
+  gap: clamp(18px, 3vw, 30px);
+}
+
+.masthead {
+  display: flex;
+  align-items: flex-end;
+  justify-content: space-between;
+  gap: 28px;
+}
+
+.wordmark {
+  min-width: 0;
+}
+
+.eyebrow {
+  margin: 0 0 4px;
+  color: var(--muted);
+  font-size: var(--text-xs);
+  font-weight: var(--weight-bold);
+  letter-spacing: 0.18em;
+  text-transform: uppercase;
+}
+
+.title {
+  margin: 0;
+  color: var(--ink);
+  font-family: var(--font-display);
+  font-size: var(--text-display);
+  font-weight: var(--weight-regular);
+  letter-spacing: -0.055em;
+  line-height: 0.82;
+}
+
+.tagline {
+  max-width: 44ch;
+  margin: 14px 0 0;
+  color: var(--muted);
+  font-size: var(--text-lg);
+  line-height: 1.45;
+}
+
+.nowrap {
+  white-space: nowrap;
+}
+
+.scores {
+  display: grid;
+  grid-template-columns: repeat(3, minmax(96px, 1fr));
+  gap: 10px;
+  flex: 0 0 auto;
+}
+
+.score-card {
+  padding: 12px 18px 14px;
+  border: 1px solid var(--line);
+  border-radius: 18px;
+  background: var(--surface);
+  box-shadow: var(--shadow-soft);
+}
+
+.score-card--best {
+  background: var(--accent-soft);
+}
+
+.score-label {
+  display: block;
+  color: var(--muted);
+  font-size: var(--text-2xs);
+  font-weight: var(--weight-bold);
+  letter-spacing: 0.16em;
+  text-transform: uppercase;
+}
+
+.score-value {
+  display: block;
+  color: var(--ink);
+  font-size: var(--text-score);
+  font-weight: var(--weight-bold);
+  font-variant-numeric: tabular-nums;
+  line-height: 1.1;
+}
+
+.game {
+  display: grid;
+  gap: 14px;
+}
+
+.board-frame {
+  position: relative;
+  padding: clamp(10px, 2.2vw, 18px);
+  border: 1px solid var(--line);
+  border-radius: 30px;
+  background: var(--surface-raised);
+  box-shadow: var(--shadow);
+}
+
+.board {
+  position: relative;
+  display: grid;
+  grid-template-columns: repeat(4, 1fr);
+  grid-template-rows: repeat(4, 1fr);
+  gap: clamp(7px, 1.4vw, 12px);
+  aspect-ratio: 1;
+  border-radius: 20px;
+  outline: none;
+}
+
+.cell {
+  position: relative;
+  min-width: 0;
+  min-height: 0;
+  border-radius: 14px;
+  background: var(--tile-empty);
+}
+
+.tile {
+  position: absolute;
+  inset: 0;
+  display: grid;
+  place-items: center;
+  border-radius: 14px;
+  font-size: var(--text-tile);
+  font-weight: var(--weight-bold);
+  font-variant-numeric: tabular-nums;
+  line-height: 1;
+  animation: tile-in 170ms ease-out both;
+}
+
+.tile--2 { background: var(--tile-2-bg); color: var(--tile-2-ink); }
+.tile--4 { background: var(--tile-4-bg); color: var(--tile-4-ink); }
+.tile--8 { background: var(--tile-8-bg); color: var(--tile-8-ink); }
+.tile--16 { background: var(--tile-16-bg); color: var(--tile-16-ink); }
+.tile--32 { background: var(--tile-32-bg); color: var(--tile-32-ink); }
+.tile--64 { background: var(--tile-64-bg); color: var(--tile-64-ink); }
+.tile--128 { background: var(--tile-128-bg); color: var(--tile-128-ink); }
+.tile--256 { background: var(--tile-256-bg); color: var(--tile-256-ink); }
+.tile--512 { background: var(--tile-512-bg); color: var(--tile-512-ink); }
+.tile--1024 { background: var(--tile-1024-bg); color: var(--tile-1024-ink); }
+.tile--2048 { background: var(--tile-2048-bg); color: var(--tile-2048-ink); }
+.tile--super { background: var(--tile-super-bg); color: var(--tile-super-ink); }
+
+@keyframes tile-in {
+  from {
+    opacity: 0.35;
+    transform: scale(0.86);
+  }
+  to {
+    opacity: 1;
+    transform: scale(1);
+  }
+}
+
+.overlay {
+  position: absolute;
+  inset: 0;
+  z-index: 2;
+  display: grid;
+  place-items: center;
+  padding: 22px;
+  border-radius: 30px;
+  background: var(--overlay);
+  backdrop-filter: blur(7px);
+}
+
+.overlay[hidden] {
+  display: none;
+}
+
+.overlay-card {
+  width: min(100%, 390px);
+  padding: clamp(22px, 4vw, 34px);
+  border: 1px solid var(--line);
+  border-radius: 22px;
+  background: var(--surface);
+  box-shadow: var(--shadow);
+  text-align: center;
+}
+
+.overlay-kicker {
+  margin: 0 0 6px;
+  color: var(--accent);
+  font-size: var(--text-2xs);
+  font-weight: var(--weight-bold);
+  letter-spacing: 0.18em;
+  text-transform: uppercase;
+}
+
+.overlay-title {
+  margin: 0;
+  color: var(--ink);
+  font-family: var(--font-display);
+  font-size: var(--text-xl);
+  font-weight: var(--weight-regular);
+  letter-spacing: -0.02em;
+}
+
+.overlay-copy {
+  margin: 10px auto 20px;
+  color: var(--muted);
+  font-size: var(--text-sm);
+}
+
+.overlay-actions {
+  display: flex;
+  flex-wrap: wrap;
+  justify-content: center;
+  gap: 10px;
+}
+
+.game-bar {
+  display: flex;
+  align-items: center;
+  justify-content: space-between;
+  gap: 18px;
+}
+
+.controls {
+  display: flex;
+  flex-wrap: wrap;
+  gap: 10px;
+}
+
+.button {
+  min-height: 42px;
+  padding: 10px 18px;
+  border: 1px solid var(--line);
+  border-radius: 999px;
+  background: var(--surface);
+  color: var(--ink);
+  cursor: pointer;
+  font-family: var(--font-sans);
+  font-size: var(--text-sm);
+  font-weight: var(--weight-bold);
+  letter-spacing: 0.01em;
+  transition: transform 120ms ease, box-shadow 120ms ease, background-color 120ms ease;
+}
+
+.button:hover {
+  transform: translateY(-1px);
+  box-shadow: var(--shadow-soft);
+}
+
+.button:active {
+  transform: translateY(0);
+}
+
+.button:focus-visible {
+  outline: 3px solid var(--focus-ring);
+  outline-offset: 3px;
+}
+
+.button--primary {
+  border-color: var(--accent-strong);
+  background: var(--accent);
+  color: var(--accent-ink);
+}
+
+.button--quiet {
+  border-color: transparent;
+  background: transparent;
+  color: var(--muted);
+}
+
+.button:disabled {
+  cursor: not-allowed;
+  opacity: 0.42;
+  transform: none;
+  box-shadow: none;
+}
+
+.hint {
+  margin: 0;
+  color: var(--muted);
+  font-size: var(--text-xs);
+  text-align: right;
+}
+
+.status {
+  min-height: 24px;
+  margin: 0;
+  color: var(--muted);
+  font-size: var(--text-sm);
+}
+
+.footer {
+  display: flex;
+  flex-wrap: wrap;
+  justify-content: space-between;
+  gap: 10px 22px;
+  padding-top: 16px;
+  border-top: 1px solid var(--line);
+  color: var(--muted);
+  font-size: var(--text-xs);
+}
+
+.footer p {
+  margin: 0;
+}
+
+.footer-mark {
+  letter-spacing: 0.08em;
+  opacity: 0.7;
+}
+
+.visually-hidden {
+  position: absolute;
+  width: 1px;
+  height: 1px;
+  margin: -1px;
+  padding: 0;
+  overflow: hidden;
+  clip: rect(0 0 0 0);
+  white-space: nowrap;
+  border: 0;
+}
+
+@media (max-width: 720px) {
+  .masthead {
+    flex-direction: column;
+    align-items: stretch;
+  }
+
+  .title {
+    font-size: var(--text-display-sm);
+  }
+
+  .scores {
+    grid-template-columns: repeat(3, minmax(0, 1fr));
+  }
+
+  .game-bar {
+    flex-direction: column;
+    align-items: stretch;
+  }
+
+  .hint {
+    text-align: left;
+  }
+
+  .footer {
+    flex-direction: column;
+  }
+}
+
+@media (prefers-reduced-motion: reduce) {
+  *,
+  *::before,
+  *::after {
+    scroll-behavior: auto;
+    animation-duration: 1ms;
+    transition-duration: 1ms;
+  }
+}
--- web/app.js ---
hunk 251bece542b0:web/app.js#1 (new lines 1..242)
@@ -0,0 +1,242 @@
+/*
+ * The browser half of Fold.
+ *
+ * It owns no rules: the Python game decides every merge, score and spawn, and this file
+ * renders the snapshot it returns. Keyboard and swipe gestures are helpers that post the
+ * same four directions the buttons and API accept.
+ */
+(function () {
+  "use strict";
+
+  var ACTIONS = { new: "new", undo: "undo", continue: "continue" };
+  var SIZE = 4;
+  var SWIPE_PX = 24;
+  var KEY_DIRECTIONS = {
+    ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right",
+    w: "up", W: "up", a: "left", A: "left", s: "down", S: "down",
+    d: "right", D: "right"
+  };
+
+  var board = document.getElementById("board");
+  var score = document.getElementById("score");
+  var best = document.getElementById("best");
+  var moves = document.getElementById("moves");
+  var undo = document.getElementById("undo");
+  var statusLine = document.getElementById("status");
+  var overlay = document.getElementById("overlay");
+  var overlayKicker = document.getElementById("overlay-kicker");
+  var overlayTitle = document.getElementById("overlay-title");
+  var overlayCopy = document.getElementById("overlay-copy");
+  var keepGoing = document.getElementById("keep-going");
+  var buttons = document.querySelectorAll("[data-action]");
+
+  var state = null;
+  var busy = false;
+  var dismissedWin = false;
+  var bestScore = readBest();
+  var touchStart = null;
+
+  function readBest() {
+    try {
+      return parseInt(window.localStorage.getItem("fold.best") || "0", 10) || 0;
+    } catch (error) {
+      return 0;
+    }
+  }
+
+  function saveBest(value) {
+    try {
+      window.localStorage.setItem("fold.best", String(value));
+    } catch (error) {
+      /* The game still works when storage is unavailable. */
+    }
+  }
+
+  function fail(error) {
+    statusLine.textContent = "Could not reach the game: " + (error.message || error) +
+      ". Is python run.py still running?";
+  }
+
+  function request(path, options) {
+    return window.fetch(path, options).then(function (response) {
+      return response.json().then(function (payload) {
+        if (!response.ok) {
+          throw new Error(payload.error || ("server returned " + response.status));
+        }
+        return payload;
+      });
+    });
+  }
+
+  function renderBoard(cells) {
+    var fragment = document.createDocumentFragment();
+    for (var index = 0; index < SIZE * SIZE; index += 1) {
+      var row = Math.floor(index / SIZE);
+      var column = index % SIZE;
+      var value = cells[row][column];
+      var cell = document.createElement("div");
+      cell.className = "cell";
+      cell.setAttribute("role", "gridcell");
+      if (value) {
+        var tile = document.createElement("div");
+        tile.className = "tile tile--" + (value <= 2048 ? value : "super");
+        tile.textContent = String(value);
+        cell.setAttribute("aria-label", "tile " + value + " at row " +
+          (row + 1) + ", column " + (column + 1));
+        cell.appendChild(tile);
+      } else {
+        cell.setAttribute("aria-label", "empty cell at row " + (row + 1) +
+          ", column " + (column + 1));
+      }
+      fragment.appendChild(cell);
+    }
+    board.textContent = "";
+    board.appendChild(fragment);
+  }
+
+  function renderOverlay() {
+    if (state.over) {
+      overlay.hidden = false;
+      overlayKicker.textContent = "board full";
+      overlayTitle.textContent = state.won ? "2048, and no moves" : "No moves left";
+      overlayCopy.textContent = "You scored " + state.score +
+        ". Start a fresh grid when you are ready.";
+      keepGoing.hidden = true;
+    } else if (state.won && !dismissedWin) {
+      overlay.hidden = false;
+      overlayKicker.textContent = "milestone";
+      overlayTitle.textContent = "2048 reached";
+      overlayCopy.textContent = "The grid bends to you. Keep going for a higher score, or start again.";
+      keepGoing.hidden = false;
+    } else {
+      overlay.hidden = true;
+      keepGoing.hidden = false;
+    }
+  }
+
+  function render(next) {
+    state = next;
+    score.textContent = String(next.score);
+    if (next.score > bestScore) {
+      bestScore = next.score;
+      saveBest(bestScore);
+    }
+    best.textContent = String(bestScore);
+    moves.textContent = String(next.moves);
+    undo.disabled = busy || !next.canUndo;
+    board.setAttribute("aria-busy", busy ? "true" : "false");
+    renderBoard(next.board);
+    renderOverlay();
+  }
+
+  function finish() {
+    busy = false;
+    if (state) {
+      undo.disabled = !state.canUndo;
+      board.setAttribute("aria-busy", "false");
+    }
+  }
+
+  function act(action) {
+    if (action === "continue") {
+      if (state) {
+        dismissedWin = true;
+        render(state);
+        statusLine.textContent = "Keep going. The next milestone is yours.";
+      }
+      return;
+    }
+    if (busy) {
+      return;
+    }
+    busy = true;
+    board.setAttribute("aria-busy", "true");
+    undo.disabled = true;
+    var path = action === "new" ? "/api/new" : "/api/undo";
+    request(path, {
+      method: "POST",
+      headers: { "Content-Type": "application/json" },
+      body: "{}"
+    }).then(function (next) {
+      if (action === "new") {
+        dismissedWin = false;
+        statusLine.textContent = "A new grid is ready.";
+      } else {
+        statusLine.textContent = "Last move undone.";
+      }
+      render(next);
+    }).catch(fail).then(finish);
+  }
+
+  function sendMove(direction) {
+    if (busy || !state || state.over || (state.won && !dismissedWin)) {
+      return;
+    }
+    busy = true;
+    board.setAttribute("aria-busy", "true");
+    undo.disabled = true;
+    request("/api/move", {
+      method: "POST",
+      headers: { "Content-Type": "application/json" },
+      body: JSON.stringify({ direction: direction })
+    }).then(function (next) {
+      render(next);
+      if (!next.moved) {
+        statusLine.textContent = "That direction is blocked.";
+      } else if (next.gained > 0) {
+        statusLine.textContent = "+" + next.gained + " points.";
+      } else {
+        statusLine.textContent = "One tile slid.";
+      }
+    }).catch(fail).then(finish);
+  }
+
+  Array.prototype.forEach.call(buttons, function (button) {
+    button.addEventListener("click", function () {
+      var action = ACTIONS[button.getAttribute("data-action")];
+      if (action) {
+        act(action);
+      }
+    });
+  });
+
+  document.addEventListener("keydown", function (event) {
+    if (event.altKey || event.ctrlKey || event.metaKey) {
+      return;
+    }
+    var direction = KEY_DIRECTIONS[event.key];
+    if (!direction || !overlay.hidden) {
+      return;
+    }
+    event.preventDefault();
+    sendMove(direction);
+  });
+
+  board.addEventListener("touchstart", function (event) {
+    if (event.touches.length !== 1) {
+      return;
+    }
+    touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
+  }, { passive: true });
+
+  board.addEventListener("touchend", function (event) {
+    if (!touchStart || !event.changedTouches.length) {
+      return;
+    }
+    var dx = event.changedTouches[0].clientX - touchStart.x;
+    var dy = event.changedTouches[0].clientY - touchStart.y;
+    touchStart = null;
+    if (Math.max(Math.abs(dx), Math.abs(dy)) < SWIPE_PX) {
+      return;
+    }
+    if (Math.abs(dx) > Math.abs(dy)) {
+      sendMove(dx > 0 ? "right" : "left");
+    } else {
+      sendMove(dy > 0 ? "down" : "up");
+    }
+  }, { passive: true });
+
+  window.fetch("/api/state", { cache: "no-store" }).then(function (response) {
+    return response.json();
+  }).then(render).catch(fail);
+})();
--- web/favicon.svg ---
hunk 251bece542b0:web/favicon.svg#1 (new lines 1..7)
@@ -0,0 +1,7 @@
+<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
+  <rect width="64" height="64" rx="14" fill="#2d2520"/>
+  <rect x="11" y="11" width="19" height="19" rx="5" fill="#d49c62"/>
+  <rect x="34" y="11" width="19" height="19" rx="5" fill="#b86135"/>
+  <rect x="11" y="34" width="19" height="19" rx="5" fill="#a54d2c"/>
+  <rect x="34" y="34" width="19" height="19" rx="5" fill="#f6c77d"/>
+</svg>
--- web/index.html ---
hunk 251bece542b0:web/index.html#1 (new lines 1..69)
@@ -0,0 +1,69 @@
+<!doctype html>
+<html lang="en" data-theme="paper">
+<head>
+<meta charset="utf-8">
+<meta name="viewport" content="width=device-width, initial-scale=1">
+<title>fold - a tile merge game</title>
+<link rel="icon" href="favicon.svg" type="image/svg+xml">
+<link rel="stylesheet" href="theme.css">
+<link rel="stylesheet" href="app.css">
+</head>
+<body>
+<div class="page">
+  <header class="masthead">
+    <div class="wordmark">
+      <p class="eyebrow" id="eyebrow">a small tile-merge game</p>
+      <h1 class="title">fold</h1>
+      <p class="tagline">Slide the grid, join matching tiles, and reach <span class="nowrap">2048</span>.</p>
+    </div>
+    <div class="scores" aria-label="game scores">
+      <div class="score-card">
+        <span class="score-label">score</span>
+        <output class="score-value" id="score">0</output>
+      </div>
+      <div class="score-card score-card--best">
+        <span class="score-label">best</span>
+        <output class="score-value" id="best">0</output>
+      </div>
+      <div class="score-card score-card--moves">
+        <span class="score-label">moves</span>
+        <output class="score-value" id="moves">0</output>
+      </div>
+    </div>
+  </header>
+
+  <section class="game" aria-labelledby="board-heading">
+    <h2 class="visually-hidden" id="board-heading">Game board</h2>
+    <div class="board-frame">
+      <div class="board" id="board" role="grid" aria-label="4 by 4 tile board" aria-busy="false"></div>
+      <div class="overlay" id="overlay" hidden>
+        <div class="overlay-card">
+          <p class="overlay-kicker" id="overlay-kicker">milestone</p>
+          <h3 class="overlay-title" id="overlay-title">2048 reached</h3>
+          <p class="overlay-copy" id="overlay-copy">The grid bends to you.</p>
+          <div class="overlay-actions">
+            <button class="button button--primary" id="overlay-new" data-action="new" type="button">New game</button>
+            <button class="button button--quiet" id="keep-going" data-action="continue" type="button">Keep going</button>
+          </div>
+        </div>
+      </div>
+    </div>
+    <div class="game-bar">
+      <div class="controls">
+        <button class="button button--primary" id="new-game" data-action="new" type="button">New game</button>
+        <button class="button" id="undo" data-action="undo" type="button" disabled>Undo</button>
+      </div>
+      <p class="hint" id="hint">Arrows / WASD to slide - swipe on touch</p>
+    </div>
+  </section>
+
+  <p class="status" id="status" role="status" aria-live="polite">A new grid is ready.</p>
+
+  <footer class="footer">
+    <p>One local Python process. No account, no network calls.</p>
+    <p class="footer-mark" aria-hidden="true">2 · 4 · 8 · 16 · 32 · 64 · 128 · 256 · 512 · 1024 · 2048</p>
+  </footer>
+</div>
+<script src="app.js"></script>
+</body>
+</html>
--- web/theme.css ---
hunk 251bece542b0:web/theme.css#1 (new lines 1..98)
@@ -0,0 +1,98 @@
+/*
+ * Every colour, font and type token Fold uses.
+ *
+ * app.css carries layout only and reads these tokens, so a literal colour or font
+ * declaration anywhere else in web/ is a style-drift finding under the UI contract.
+ */
+
+:root {
+  color-scheme: light;
+  --font-sans: "Segoe UI", "Avenir Next", "Helvetica Neue", Arial, sans-serif;
+  --font-display: Georgia, "Iowan Old Style", "Times New Roman", serif;
+  --weight-regular: 400;
+  --weight-medium: 550;
+  --weight-bold: 700;
+  --text-2xs: 0.68rem;
+  --text-xs: 0.76rem;
+  --text-sm: 0.88rem;
+  --text-md: 1rem;
+  --text-lg: 1.18rem;
+  --text-xl: 1.55rem;
+  --text-score: clamp(1.5rem, 4vw, 2.1rem);
+  --text-tile: clamp(1.15rem, 4.4vw, 2rem);
+  --text-display: clamp(4.2rem, 14vw, 8.4rem);
+  --text-display-sm: clamp(3.4rem, 18vw, 5.2rem);
+  --paper: #f3ede2;
+  --paper-soft: #faf6ed;
+  --surface: #fffaf1;
+  --surface-raised: #fffdf8;
+  --ink: #2e2822;
+  --muted: #776b5d;
+  --line: rgba(46, 40, 34, 0.12);
+  --accent: #b8552b;
+  --accent-strong: #8f3d1c;
+  --accent-ink: #fff8ef;
+  --accent-soft: rgba(184, 85, 43, 0.12);
+  --glow-a: rgba(210, 154, 99, 0.26);
+  --glow-b: rgba(120, 144, 112, 0.16);
+  --shadow: 0 28px 70px rgba(59, 46, 33, 0.16);
+  --shadow-soft: 0 10px 28px rgba(59, 46, 33, 0.09);
+  --focus-ring: #2f6f6a;
+  --tile-empty: rgba(46, 40, 34, 0.065);
+  --overlay: rgba(250, 246, 237, 0.78);
+  --tile-2-bg: #eee3cf;
+  --tile-2-ink: #4c4237;
+  --tile-4-bg: #e8d4b5;
+  --tile-4-ink: #4c3d2d;
+  --tile-8-bg: #dfb783;
+  --tile-8-ink: #4a321d;
+  --tile-16-bg: #d49c62;
+  --tile-16-ink: #3f2815;
+  --tile-32-bg: #c77d49;
+  --tile-32-ink: #fff6ea;
+  --tile-64-bg: #b86135;
+  --tile-64-ink: #fff4e7;
+  --tile-128-bg: #a54d2c;
+  --tile-128-ink: #fff1e1;
+  --tile-256-bg: #8d3c26;
+  --tile-256-ink: #ffeeda;
+  --tile-512-bg: #74301f;
+  --tile-512-ink: #ffe8d0;
+  --tile-1024-bg: #58251a;
+  --tile-1024-ink: #ffd9ae;
+  --tile-2048-bg: #2d2520;
+  --tile-2048-ink: #f6c77d;
+  --tile-super-bg: #1f1a17;
+  --tile-super-ink: #ffd9a0;
+}
+
+@media (prefers-color-scheme: dark) {
+  :root {
+    color-scheme: dark;
+    --paper: #1c1916;
+    --paper-soft: #24201c;
+    --surface: #2a2520;
+    --surface-raised: #322b25;
+    --ink: #f2e8d9;
+    --muted: #b8a897;
+    --line: rgba(242, 232, 217, 0.14);
+    --accent: #d4784b;
+    --accent-strong: #e89a6f;
+    --accent-ink: #201610;
+    --accent-soft: rgba(212, 120, 75, 0.16);
+    --glow-a: rgba(212, 120, 75, 0.18);
+    --glow-b: rgba(112, 145, 123, 0.14);
+    --shadow: 0 28px 70px rgba(0, 0, 0, 0.45);
+    --shadow-soft: 0 10px 28px rgba(0, 0, 0, 0.3);
+    --focus-ring: #7fc7bd;
+    --tile-empty: rgba(242, 232, 217, 0.08);
+    --overlay: rgba(28, 25, 22, 0.82);
+  }
+}
+
+button,
+output {
+  font-family: var(--font-sans);
+  font-size: var(--text-md);
+  font-weight: var(--weight-medium);
+}