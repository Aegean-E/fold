"""
One game in memory: a board, a score, and a short undo trail.

The server owns exactly one `Game` and serializes every call to it. Keeping the state
here rather than in the browser means a reload cannot show a board the rules would
reject, and every transition is exercised by the unit tests without a socket.

PRINCIPLE-003, PRINCIPLE-009, PRINCIPLE-013, PRINCIPLE-014.
"""

import random
from typing import Dict, List, Optional, Tuple

from fold.board import Board, empty_board, has_moves, has_won, move as slide, spawn

HISTORY_LIMIT = 20


class Game:
    """A tile-merge game with one-level-or-more undo and a JSON-ready read model."""

    def __init__(self, rng: Optional[random.Random] = None,
                 board: Optional[Board] = None) -> None:
        self._rng = rng or random.Random()
        self._board = board if board is not None else self._starting_board()
        self._score = 0
        self._history: List[Tuple[Board, int]] = []
        self._moves = 0

    def reset(self) -> Dict[str, object]:
        """Start a fresh game with two tiles and no undo history."""
        self._board = self._starting_board()
        self._score = 0
        self._history = []
        self._moves = 0
        return self.state()

    def move(self, direction: str) -> Dict[str, object]:
        """
        Apply one direction, spawn one tile after a real move, and report the outcome.

        A blocked direction changes nothing and does not spawn or charge a move.
        """
        after, gained = slide(self._board, direction)
        moved = after != self._board
        if not moved:
            return self.state(moved=False, gained=0)
        self._remember()
        self._board = spawn(after, self._rng)
        self._score += gained
        self._moves += 1
        return self.state(moved=True, gained=gained)

    def undo(self) -> Dict[str, object]:
        """Restore the board and score before the last real move, if there is one."""
        if not self._history:
            return self.state()
        self._board, self._score = self._history.pop()
        self._moves = max(0, self._moves - 1)
        return self.state()

    def state(self, moved: Optional[bool] = None,
              gained: int = 0) -> Dict[str, object]:
        """The flat read model the HTTP layer and the browser both consume."""
        return {
            "board": [list(row) for row in self._board],
            "score": self._score,
            "won": has_won(self._board),
            "over": not has_moves(self._board),
            "canUndo": bool(self._history),
            "moves": self._moves,
            "moved": moved,
            "gained": gained,
        }

    def _starting_board(self) -> Board:
        """Two tiles placed by the game's own random source."""
        return spawn(spawn(empty_board(), self._rng), self._rng)

    def _remember(self) -> None:
        """Keep the pre-move state for undo, bounded so a long game cannot grow forever."""
        self._history.append((self._board, self._score))
        if len(self._history) > HISTORY_LIMIT:
            self._history.pop(0)
