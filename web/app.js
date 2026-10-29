/*
 * The browser half of Fold.
 *
 * It owns no rules: the Python game decides every merge, score and spawn, and this file
 * renders the snapshot it returns. Keyboard and swipe gestures are helpers that post the
 * same four directions the buttons and API accept.
 */
(function () {
  "use strict";

  var ACTIONS = { new: "new", undo: "undo", continue: "continue" };
  var SIZE = 4;
  var SWIPE_PX = 24;
  var KEY_DIRECTIONS = {
    ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right",
    w: "up", W: "up", a: "left", A: "left", s: "down", S: "down",
    d: "right", D: "right"
  };

  var board = document.getElementById("board");
  var score = document.getElementById("score");
  var best = document.getElementById("best");
  var moves = document.getElementById("moves");
  var undo = document.getElementById("undo");
  var statusLine = document.getElementById("status");
  var overlay = document.getElementById("overlay");
  var overlayKicker = document.getElementById("overlay-kicker");
  var overlayTitle = document.getElementById("overlay-title");
  var overlayCopy = document.getElementById("overlay-copy");
  var keepGoing = document.getElementById("keep-going");
  var buttons = document.querySelectorAll("[data-action]");

  var state = null;
  var busy = false;
  var dismissedWin = false;
  var bestScore = readBest();
  var touchStart = null;

  function readBest() {
    try {
      return parseInt(window.localStorage.getItem("fold.best") || "0", 10) || 0;
    } catch (error) {
      return 0;
    }
  }

  function saveBest(value) {
    try {
      window.localStorage.setItem("fold.best", String(value));
    } catch (error) {
      /* The game still works when storage is unavailable. */
    }
  }

  function fail(error) {
    statusLine.textContent = "Could not reach the game: " + (error.message || error) +
      ". Is python run.py still running?";
  }

  function request(path, options) {
    return window.fetch(path, options).then(function (response) {
      return response.json().then(function (payload) {
        if (!response.ok) {
          throw new Error(payload.error || ("server returned " + response.status));
        }
        return payload;
      });
    });
  }

  function renderBoard(cells) {
    var fragment = document.createDocumentFragment();
    for (var index = 0; index < SIZE * SIZE; index += 1) {
      var row = Math.floor(index / SIZE);
      var column = index % SIZE;
      var value = cells[row][column];
      var cell = document.createElement("div");
      cell.className = "cell";
      cell.setAttribute("role", "gridcell");
      if (value) {
        var tile = document.createElement("div");
        tile.className = "tile tile--" + (value <= 2048 ? value : "super");
        tile.textContent = String(value);
        cell.setAttribute("aria-label", "tile " + value + " at row " +
          (row + 1) + ", column " + (column + 1));
        cell.appendChild(tile);
      } else {
        cell.setAttribute("aria-label", "empty cell at row " + (row + 1) +
          ", column " + (column + 1));
      }
      fragment.appendChild(cell);
    }
    board.textContent = "";
    board.appendChild(fragment);
  }

  function renderOverlay() {
    if (state.over) {
      overlay.hidden = false;
      overlayKicker.textContent = "board full";
      overlayTitle.textContent = state.won ? "2048, and no moves" : "No moves left";
      overlayCopy.textContent = "You scored " + state.score +
        ". Start a fresh grid when you are ready.";
      keepGoing.hidden = true;
    } else if (state.won && !dismissedWin) {
      overlay.hidden = false;
      overlayKicker.textContent = "milestone";
      overlayTitle.textContent = "2048 reached";
      overlayCopy.textContent = "The grid bends to you. Keep going for a higher score, or start again.";
      keepGoing.hidden = false;
    } else {
      overlay.hidden = true;
      keepGoing.hidden = false;
    }
  }

  function render(next) {
    state = next;
    score.textContent = String(next.score);
    if (next.score > bestScore) {
      bestScore = next.score;
      saveBest(bestScore);
    }
    best.textContent = String(bestScore);
    moves.textContent = String(next.moves);
    undo.disabled = busy || !next.canUndo;
    board.setAttribute("aria-busy", busy ? "true" : "false");
    renderBoard(next.board);
    renderOverlay();
  }

  function finish() {
    busy = false;
    if (state) {
      undo.disabled = !state.canUndo;
      board.setAttribute("aria-busy", "false");
    }
  }

  function act(action) {
    if (action === "continue") {
      if (state) {
        dismissedWin = true;
        render(state);
        statusLine.textContent = "Keep going. The next milestone is yours.";
      }
      return;
    }
    if (busy) {
      return;
    }
    busy = true;
    board.setAttribute("aria-busy", "true");
    undo.disabled = true;
    var path = action === "new" ? "/api/new" : "/api/undo";
    request(path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "{}"
    }).then(function (next) {
      if (action === "new") {
        dismissedWin = false;
        statusLine.textContent = "A new grid is ready.";
      } else {
        statusLine.textContent = "Last move undone.";
      }
      render(next);
    }).catch(fail).then(finish);
  }

  function sendMove(direction) {
    if (busy || !state || state.over || (state.won && !dismissedWin)) {
      return;
    }
    busy = true;
    board.setAttribute("aria-busy", "true");
    undo.disabled = true;
    request("/api/move", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ direction: direction })
    }).then(function (next) {
      render(next);
      if (!next.moved) {
        statusLine.textContent = "That direction is blocked.";
      } else if (next.gained > 0) {
        statusLine.textContent = "+" + next.gained + " points.";
      } else {
        statusLine.textContent = "One tile slid.";
      }
    }).catch(fail).then(finish);
  }

  Array.prototype.forEach.call(buttons, function (button) {
    button.addEventListener("click", function () {
      var action = ACTIONS[button.getAttribute("data-action")];
      if (action) {
        act(action);
      }
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.altKey || event.ctrlKey || event.metaKey) {
      return;
    }
    var direction = KEY_DIRECTIONS[event.key];
    if (!direction || !overlay.hidden) {
      return;
    }
    event.preventDefault();
    sendMove(direction);
  });

  board.addEventListener("touchstart", function (event) {
    if (event.touches.length !== 1) {
      return;
    }
    touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
  }, { passive: true });

  board.addEventListener("touchend", function (event) {
    if (!touchStart || !event.changedTouches.length) {
      return;
    }
    var dx = event.changedTouches[0].clientX - touchStart.x;
    var dy = event.changedTouches[0].clientY - touchStart.y;
    touchStart = null;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < SWIPE_PX) {
      return;
    }
    if (Math.abs(dx) > Math.abs(dy)) {
      sendMove(dx > 0 ? "right" : "left");
    } else {
      sendMove(dy > 0 ? "down" : "up");
    }
  }, { passive: true });

  board.addEventListener("touchcancel", function () {
    touchStart = null;
  }, { passive: true });

  window.fetch("/api/state", { cache: "no-store" }).then(function (response) {
    return response.json();
  }).then(render).catch(fail);
})();
