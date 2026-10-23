"""
The pure board rules of Fold.

A board is a tuple of four rows; zero means empty. Nothing here knows about HTTP, random
seeds or the browser: `move` and `slide_row` are deterministic, and `spawn` takes the
random source as an argument so a test can replay a game exactly.

PRINCIPLE-003, PRINCIPLE-009, PRINCIPLE-014.
"""

import random
from typing import List, Sequence, Tuple

SIZE = 4
WINNING_VALUE = 2048
DIRECTIONS = ("up", "down", "left", "right")
Board = Tuple[Tuple[int, ...], ...]


def empty_board() -> Board:
    """A 4x4 board with no tiles."""
    return tuple((0,) * SIZE for _ in range(SIZE))


def slide_row(row: Sequence[int]) -> Tuple[Tuple[int, ...], int]:
    """
    Slide one row toward index zero, merging equal neighbours once, left to right.

    Returns the new row and the points earned. `[2, 2, 2, 2]` becomes `[4, 4, 0, 0]`
    and earns 8; a merged tile never merges again on the same slide.
    """
    tiles = [value for value in row if value]
    merged: List[int] = []
    gained = 0
    index = 0
    while index < len(tiles):
        if index + 1 < len(tiles) and tiles[index] == tiles[index + 1]:
            value = tiles[index] * 2
            merged.append(value)
            gained += value
            index += 2
        else:
            merged.append(tiles[index])
            index += 1
    merged.extend([0] * (SIZE - len(merged)))
    return tuple(merged), gained


def move(board: Board, direction: str) -> Tuple[Board, int]:
    """
    Slide every tile in `direction`; return the new board and the points earned.

    An unknown direction raises `ValueError`, so a bad request never mutates a game.
    """
    if direction not in DIRECTIONS:
        raise ValueError(f"direction must be one of {', '.join(DIRECTIONS)}")
    if direction == "left":
        return _slide_rows(board)
    if direction == "right":
        flipped, gained = _slide_rows(_flip_rows(board))
        return _flip_rows(flipped), gained
    if direction == "up":
        transposed, gained = _slide_rows(_transpose(board))
        return _transpose(transposed), gained
    transposed, gained = _slide_rows(_flip_rows(_transpose(board)))
    return _transpose(_flip_rows(transposed)), gained


def spawn(board: Board, rng: random.Random, count: int = 1) -> Board:
    """
    Place `count` new tiles (90% a 2, 10% a 4) in empty cells chosen by `rng`.

    When fewer empty cells exist than `count`, every empty cell is filled.
    """
    cells = [(row, column) for row in range(SIZE) for column in range(SIZE)
             if board[row][column] == 0]
    rng.shuffle(cells)
    updated = [list(row) for row in board]
    for row, column in cells[:max(0, count)]:
        updated[row][column] = 4 if rng.random() < 0.1 else 2
    return tuple(tuple(row) for row in updated)


def has_won(board: Board, target: int = WINNING_VALUE) -> bool:
    """Whether any tile has reached the winning value."""
    return any(value >= target for row in board for value in row)


def has_moves(board: Board) -> bool:
    """Whether an empty cell or an equal orthogonal neighbour leaves a move available."""
    for row in range(SIZE):
        for column in range(SIZE):
            value = board[row][column]
            if value == 0:
                return True
            if column + 1 < SIZE and board[row][column + 1] == value:
                return True
            if row + 1 < SIZE and board[row + 1][column] == value:
                return True
    return False


def _slide_rows(board: Board) -> Tuple[Board, int]:
    """Slide every row toward index zero and sum the points."""
    rows: List[Tuple[int, ...]] = []
    gained = 0
    for row in board:
        slid, points = slide_row(row)
        rows.append(slid)
        gained += points
    return tuple(rows), gained


def _transpose(board: Board) -> Board:
    """Swap rows and columns."""
    return tuple(tuple(board[row][column] for row in range(SIZE)) for column in range(SIZE))


def _flip_rows(board: Board) -> Board:
    """Mirror every row left to right."""
    return tuple(tuple(reversed(row)) for row in board)
