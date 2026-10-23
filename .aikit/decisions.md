# Decisions

Why this project is built the way it is, oldest first. One entry per decision that changes a
contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.

<!-- Entry format:
### ADR-NNN: <decision in one line>
- **Date**: YYYY-MM-DD
- **Status**: Accepted
- **Context**: <what forced the decision>
- **Decision**: <what was decided>
- **Consequences**: <what follows, including what it costs>
-->

### ADR-001: The server owns the rules; the browser owns only the rendering
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: A tile-merge game has enough rules (merge-once, spawn, score, win, game over) that a second browser implementation would drift from the tested one.
- **Decision**: `fold/board.py` holds pure rules and `fold/game.py` holds one game's state and undo trail. `fold/server.py` translates four JSON endpoints into those calls; `web/app.js` renders the returned snapshot and posts a direction.
- **Consequences**: Every rule is tested in Python without a browser, and a reload cannot show a board the rules would reject. The cost is one loopback round trip per move, which is negligible for a turn-based local game.

### ADR-002: One lock serializes game mutations on a threaded local server
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: The browser can issue a move while another tab polls the state, and a race could spawn two tiles or lose an undo entry.
- **Decision**: `FoldHTTPServer` is thread-per-request, while every `Game` read and mutation runs under one `threading.Lock` held by the request handler.
- **Consequences**: State transitions are atomic and the game stays simple; concurrent reads serialize for microseconds. The lock is not a persistence layer: the game vanishes when the process stops.

### ADR-003: The snapshot proof is a parsed inventory, not a rendered screenshot
- **Date**: 2026-10-22
- **Status**: Accepted
- **Context**: The UI guard needs a stable way to notice a dropped control, action, handler or theme token, but Fold declares no browser or Node dependency.
- **Decision**: `tools/ui_inventory.py` parses `web/` and prints one line per identified element, named action, ARIA role, live region, script handler and theme token. `tools/dogfood.py` covers the served page and the API over a real socket.
- **Consequences**: A dropped control or token is a lost inventory line and accessibility attributes are guarded alongside controls. A purely visual regression that keeps the inventory intact is not caught; that is the deliberate price of a zero-dependency surface.

### ADR-004: Fold listens on 8766, not the workspace's other local port
- **Date**: 2026-10-23
- **Status**: Accepted
- **Context**: A previous local server process can keep port 8765 open for hours. Fold's old default collided with it, so opening `http://127.0.0.1:8765` showed that other application instead of the game, and the browser had no way to tell the difference.
- **Decision**: `DEFAULT_PORT` is `8766`. The port stays fixed, so the browser's local-storage best score remains on one origin, and `--port` still accepts any free port from 1 to 65535.
- **Consequences**: One-click launchers open Fold without a collision when the other local tool owns 8765. A second Fold instance on 8766 exits with a Why/Fix message instead of opening a different page; the same message appears for any other occupied port.
