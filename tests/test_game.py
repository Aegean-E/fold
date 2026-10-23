"""One game's state transitions: start, move, undo and terminal read model."""

import random
import unittest

from fold.board import empty_board
from fold.game import Game

START = ((2, 2, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
LOCKED = ((2, 4, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))


class GameTest(unittest.TestCase):

    def test_a_new_game_has_two_tiles_and_no_history(self):
        game = Game(random.Random(5))
        state = game.state()
        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
        self.assertEqual(0, state["score"])
        self.assertFalse(state["canUndo"])
        self.assertEqual(0, state["moves"])

    def test_a_move_merges_scores_and_spawns_exactly_one_tile(self):
        game = Game(random.Random(2), board=START)
        state = game.move("left")
        self.assertTrue(state["moved"])
        self.assertEqual(4, state["score"])
        self.assertEqual(4, state["gained"])
        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))
        self.assertEqual(1, state["moves"])
        self.assertTrue(state["canUndo"])

    def test_a_blocked_direction_changes_nothing(self):
        game = Game(random.Random(2), board=LOCKED)
        before = game.state()
        after = game.move("left")
        self.assertFalse(after["moved"])
        self.assertEqual(before["board"], after["board"])
        self.assertEqual(0, after["score"])
        self.assertEqual(0, after["moves"])
        self.assertFalse(after["canUndo"])

    def test_undo_restores_the_board_and_score(self):
        game = Game(random.Random(2), board=START)
        before = game.state()
        game.move("left")
        restored = game.undo()
        self.assertEqual(before["board"], restored["board"])
        self.assertEqual(before["score"], restored["score"])
        self.assertFalse(restored["canUndo"])

    def test_reset_deals_a_new_board_and_clears_history(self):
        game = Game(random.Random(2), board=START)
        game.move("left")
        state = game.reset()
        self.assertEqual(0, state["score"])
        self.assertEqual(0, state["moves"])
        self.assertFalse(state["canUndo"])
        self.assertEqual(2, sum(1 for row in state["board"] for value in row if value))

    def test_a_full_checkerboard_reports_game_over(self):
        board = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
        state = Game(random.Random(1), board=board).state()
        self.assertTrue(state["over"])
        self.assertFalse(state["won"])

    def test_a_2048_tile_reports_a_win(self):
        board = ((2048, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        state = Game(random.Random(1), board=board).state()
        self.assertTrue(state["won"])
        self.assertFalse(state["over"])

    def test_state_has_the_declared_json_shape(self):
        state = Game(random.Random(1), board=empty_board()).state(moved=True, gained=8)
        self.assertEqual({"board", "score", "won", "over", "canUndo", "moves", "moved", "gained"},
                         set(state))
        self.assertTrue(state["moved"])
        self.assertEqual(8, state["gained"])


if __name__ == "__main__":
    unittest.main()
