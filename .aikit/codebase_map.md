# Codebase Map & Symbol Catalog 🗺️

> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.

---

## 📊 Codebase Metrics
- **Total Python Modules**: `17`
- **Total Classes**: `18`
- **Total Top-Level Functions**: `29`
- **Total Class Methods**: `72`
- **Total Source Lines**: `1283`

---

## 📦 Modules & Exported Symbols

### [`fold/__init__.py`](fold/__init__.py)
> *Fold: a small 4x4 tile-merge game with a local browser surface.*

**Size**: `3` lines (`93` bytes)

---

### [`fold/__main__.py`](fold/__main__.py)
> *Allow `python -m fold` as the same entry point as `python run.py`.*

**Size**: `8` lines (`161` bytes)

---

### [`fold/board.py`](fold/board.py)
> *The pure board rules of Fold.*

**Size**: `121` lines (`4106` bytes)

**Functions:**
- `def empty_board()` - *A 4x4 board with no tiles.*
- `def slide_row(row)` - *Slide one row toward index zero, merging equal neighbours once, left to right.*
- `def move(board, direction)` - *Slide every tile in `direction`; return the new board and the points earned.*
- `def spawn(board, rng, count)` - *Place `count` new tiles (90% a 2, 10% a 4) in empty cells chosen by `rng`.*
- `def has_won(board, target)` - *Whether any tile has reached the winning value.*
- `def has_moves(board)` - *Whether an empty cell or an equal orthogonal neighbour leaves a move available.*
- `def _slide_rows(board)` - *Slide every row toward index zero and sum the points.*
- `def _transpose(board)` - *Swap rows and columns.*
- `def _flip_rows(board)` - *Mirror every row left to right.*

---

### [`fold/cli.py`](fold/cli.py)
> *Start Fold and print the one URL a user needs.*

**Size**: `86` lines (`3461` bytes)

**Classes:**
- `class TriadParser` - *Argparse that adds AIKit's Why/Fix triad to a bad flag (PRINCIPLE-011 R5).*
  - Method `.error(message)` - *Print usage and a triad, then exit 2 without opening a socket.*

**Functions:**
- `def port_number(text)` - *Argparse type for a TCP port, with a message a person can act on.*
- `def parse_args(argv)` - *The command line: local host, port, optional seed and optional browser open.*
- `def main(argv)` - *Serve until interrupted; 0 on a clean stop, 1 on a bind failure, 2 on bad flags.*

---

### [`fold/game.py`](fold/game.py)
> *One game in memory: a board, a score, and a short undo trail.*

**Size**: `84` lines (`3117` bytes)

**Classes:**
- `class Game` - *A tile-merge game with one-level-or-more undo and a JSON-ready read model.*
  - Method `.__init__(rng, board)`
  - Method `.reset()` - *Start a fresh game with two tiles and no undo history.*
  - Method `.move(direction)` - *Apply one direction, spawn one tile after a real move, and report the outcome.*
  - Method `.undo()` - *Restore the board and score before the last real move, if there is one.*
  - Method `.state(moved, gained)` - *The flat read model the HTTP layer and the browser both consume.*
  - Method `._starting_board()` - *Two tiles placed by the game's own random source.*
  - Method `._remember()` - *Keep the pre-move state for undo, bounded so a long game cannot grow forever.*

---

### [`fold/server.py`](fold/server.py)
> *The local HTTP layer: static files from `web/` and four JSON endpoints.*

**Size**: `168` lines (`6578` bytes)

**Classes:**
- `class StaticFiles` - *Resolves a URL path to a file inside one directory, and never outside it.*
  - Method `.resolve(url_path)` - *The file a decoded URL path names, or None when it escapes or does not exist.*
- `class FoldHandler` - *Translates requests into `Game` reads and mutations.*
  - Method `.do_GET()`
  - Method `.do_POST()`
  - Method `._payload(raw)` - *Decode one JSON object; anything else is a 400, never a traceback.*
  - Method `._act(route, payload)` - *Apply one named endpoint to the game and return its read model.*
  - Method `._json(status, payload)`
  - Method `._respond(status, content_type, body, cache)`
  - Method `.end_headers()` - *Attach the security policy to every response, including stdlib errors.*
  - Method `.log_message(format, *args)` - *Silent by default; `fold.cli` prints the one line a user needs.*
- `class FoldHTTPServer` - *A local thread-per-request server whose threads do not outlive the process.*

**Functions:**
- `def build_server(game, port, web, host)` - *An HTTP server bound to `host:port`, serving `web` and one in-memory game.*

---

### [`run.py`](run.py)
> *The user-facing entry point: `python run.py` starts Fold on port 8766.*

**Size**: `9` lines (`188` bytes)

---

### [`tests/__init__.py`](tests/__init__.py)
> *Fold's test package.*

**Size**: `1` lines (`27` bytes)

---

### [`tests/test_board.py`](tests/test_board.py)
> *Pure board rules: sliding, merging, spawning and terminal detection.*

**Size**: `85` lines (`3398` bytes)

**Classes:**
- `class SlideRowTest`
  - Method `.test_equal_neighbours_merge_once_and_earn_their_sum()`
  - Method `.test_zeros_compact_before_merging()`
  - Method `.test_a_merged_tile_never_merges_again_in_the_same_slide()`
  - Method `.test_a_row_with_no_pair_only_compacts()`
- `class MoveTest`
  - Method `.test_left_and_right_are_mirror_images()`
  - Method `.test_up_and_down_are_mirror_images()`
  - Method `.test_an_unknown_direction_is_refused()`
- `class SpawnTest`
  - Method `.test_spawn_places_the_requested_number_of_tiles_in_empty_cells()`
  - Method `.test_spawn_with_a_shared_seed_is_replayable()`
  - Method `.test_spawn_never_overwrites_a_tile()`
- `class TerminalTest`
  - Method `.test_winning_value_is_detected()`
  - Method `.test_an_empty_cell_leaves_a_move()`
  - Method `.test_a_full_checkerboard_has_no_moves()`
  - Method `.test_a_full_board_with_an_equal_neighbour_still_moves()`

---

### [`tests/test_cli.py`](tests/test_cli.py)
> *Command-line parsing: local defaults, an optional seed and a validated port.*

**Size**: `44` lines (`1387` bytes)

**Classes:**
- `class CliTest`
  - Method `.test_defaults_keep_the_game_local()`
  - Method `.test_a_seed_and_open_are_opt_in()`
  - Method `.test_a_port_outside_the_valid_range_is_refused()`
  - Method `.test_a_valid_port_is_an_integer()`
  - Method `.test_a_bad_flag_exits_two_with_a_triad()`

---

### [`tests/test_game.py`](tests/test_game.py)
> *One game's state transitions: start, move, undo and terminal read model.*

**Size**: `82` lines (`3244` bytes)

**Classes:**
- `class GameTest`
  - Method `.test_a_new_game_has_two_tiles_and_no_history()`
  - Method `.test_a_move_merges_scores_and_spawns_exactly_one_tile()`
  - Method `.test_a_blocked_direction_changes_nothing()`
  - Method `.test_undo_restores_the_board_and_score()`
  - Method `.test_reset_deals_a_new_board_and_clears_history()`
  - Method `.test_a_full_checkerboard_reports_game_over()`
  - Method `.test_a_2048_tile_reports_a_win()`
  - Method `.test_state_has_the_declared_json_shape()`

---

### [`tests/test_inventory.py`](tests/test_inventory.py)
> *The UI inventory proof covers the controls, handlers, live region and theme tokens.*

**Size**: `29` lines (`983` bytes)

**Classes:**
- `class InventoryTest`
  - Method `.test_the_inventory_names_the_controls_and_theme_tokens()`
  - Method `.test_the_page_and_script_are_part_of_the_surface()`

---

### [`tests/test_launchers.py`](tests/test_launchers.py)
> *One-click launch files: present, CRLF-safe on Windows and pointing at run.py.*

**Size**: `45` lines (`1819` bytes)

**Classes:**
- `class LauncherTest`
  - Method `.test_every_launcher_exists()`
  - Method `.test_batch_files_have_crlf_line_endings()`
  - Method `.test_launchers_start_the_game_and_aliases_delegate()`
  - Method `.test_a_batch_failure_stays_visible()`
  - Method `.test_gitattributes_pins_launcher_line_endings()`

---

### [`tests/test_server.py`](tests/test_server.py)
> *The HTTP layer over a real socket: JSON endpoints, static files and hostile input.*

**Size**: `138` lines (`5734` bytes)

**Classes:**
- `class ServerHarness` - *One server on an ephemeral port, torn down without a lingering thread.*
  - Method `.__init__(board)`
  - Method `.close()`
  - Method `.request(path, payload)`
- `class ServerTest`
  - Method `.setUp()`
  - Method `.test_the_page_and_assets_are_served()`
  - Method `.test_security_headers_are_present()`
  - Method `.test_state_returns_the_declared_shape()`
  - Method `.test_a_move_merges_and_spawns_a_tile()`
  - Method `.test_undo_restores_the_previous_board()`
  - Method `.test_a_bad_direction_is_a_400_with_an_error()`
  - Method `.test_malformed_json_is_a_400()`
  - Method `.test_an_oversized_body_is_a_413()`
  - Method `.test_an_unknown_route_is_a_json_404()`
  - Method `.test_a_trailing_slash_is_not_the_index()`
- `class StaticFilesTest`
  - Method `.setUp()`
  - Method `.test_root_serves_the_index()`
  - Method `.test_paths_outside_the_web_root_are_refused()`

---

### [`tools/__init__.py`](tools/__init__.py)
> *Developer proofs for Fold.*

**Size**: `1` lines (`33` bytes)

---

### [`tools/dogfood.py`](tools/dogfood.py)
> *Fold's dogfood runner: play it the way a user does, then attack the surface.*

**Size**: `278` lines (`11372` bytes)

**Classes:**
- `class Report` - *Collects step outcomes: the console sees a summary, the log sees everything.*
  - Method `.__init__()`
  - Method `.step(ok, label, detail)` - *Record one step's outcome and hand back whether it passed.*

**Functions:**
- `def terminate_process_tree(process)` - *Kill a process and everything it started, on Windows and POSIX alike.*
- `def supervised(command, log)` - *Run a command with stdin closed, killing its whole tree on the way out.*
- `def free_port()` - *A port the operating system says is free right now.*
- `def fingerprint()` - *A digest of every tracked file, so a run that dirties the repository fails.*
- `def get(base, path)` - *One GET, with the milliseconds it took.*
- `def post(base, path, payload, raw)` - *One POST; an HTTP error is an answer here, not an exception.*
- `def wait_until_serving(base)` - *True once the server answers, False if it never does within the start timeout.*
- `def golden_path(base, report)` - *Load the page, make a move, undo it and read the state back.*
- `def chaos(base, report)` - *Hostile input: malformed JSON, bad directions, a flood and traversal.*
- `def surface_proof(report, log)` - *The UI inventory proof runs and reports its surface, as the UI guard expects.*
- `def main()` - *Run both tracks in one sandbox and print at most 15 lines.*

---

### [`tools/ui_inventory.py`](tools/ui_inventory.py)
> *Print Fold's UI inventory, one entry per line.*

**Size**: `101` lines (`3666` bytes)

**Classes:**
- `class SurfaceParser` - *Collects identified elements, named actions and live regions of one page.*
  - Method `.__init__()`
  - Method `.handle_starttag(tag, attrs)`

**Functions:**
- `def html_entries(path)` - *Identified elements, actions, roles and live regions declared in a page.*
- `def handler_entries(path)` - *Action names the browser script is willing to dispatch.*
- `def token_entries(path)` - *Theme custom properties the stylesheet declares.*
- `def inventory(web)` - *Every inventory entry of a web directory, sorted and deduplicated.*
- `def main(argv)` - *Write the inventory to stdout; exit 1 when the surface has no entries at all.*

---
