"""Pure board rules: sliding, merging, spawning and terminal detection."""

import random
import unittest

from fold.board import (empty_board, has_moves, has_won, move, slide_row, spawn)


class SlideRowTest(unittest.TestCase):

    def test_equal_neighbours_merge_once_and_earn_their_sum(self):
        self.assertEqual(((4, 4, 0, 0), 8), slide_row((2, 2, 2, 2)))

    def test_zeros_compact_before_merging(self):
        self.assertEqual(((4, 0, 0, 0), 4), slide_row((0, 2, 0, 2)))

    def test_a_merged_tile_never_merges_again_in_the_same_slide(self):
        self.assertEqual(((8, 8, 0, 0), 8), slide_row((4, 4, 8, 0)))

    def test_a_row_with_no_pair_only_compacts(self):
        self.assertEqual(((2, 4, 8, 0), 0), slide_row((0, 2, 4, 8)))


class MoveTest(unittest.TestCase):

    def test_left_and_right_are_mirror_images(self):
        board = ((2, 0, 2, 4), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        left, left_points = move(board, "left")
        right, right_points = move(board, "right")
        self.assertEqual(((4, 4, 0, 0),) + ((0, 0, 0, 0),) * 3, left)
        self.assertEqual(((0, 0, 4, 4),) + ((0, 0, 0, 0),) * 3, right)
        self.assertEqual((left_points, right_points), (4, 4))

    def test_up_and_down_are_mirror_images(self):
        board = ((2, 0, 0, 0), (2, 0, 0, 0), (4, 0, 0, 0), (0, 0, 0, 0))
        up, up_points = move(board, "up")
        down, down_points = move(board, "down")
        self.assertEqual(((4, 0, 0, 0), (4, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)), up)
        self.assertEqual(((0, 0, 0, 0), (0, 0, 0, 0), (4, 0, 0, 0), (4, 0, 0, 0)), down)
        self.assertEqual((up_points, down_points), (4, 4))

    def test_an_unknown_direction_is_refused(self):
        with self.assertRaisesRegex(ValueError, "direction must be one of"):
            move(empty_board(), "sideways")


class SpawnTest(unittest.TestCase):

    def test_spawn_places_the_requested_number_of_tiles_in_empty_cells(self):
        board = spawn(empty_board(), random.Random(3), count=2)
        values = [value for row in board for value in row]
        self.assertEqual(2, sum(1 for value in values if value))
        self.assertTrue(all(value in (0, 2, 4) for value in values))

    def test_spawn_with_a_shared_seed_is_replayable(self):
        first = spawn(empty_board(), random.Random(11), count=3)
        second = spawn(empty_board(), random.Random(11), count=3)
        self.assertEqual(first, second)

    def test_spawn_never_overwrites_a_tile(self):
        full = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
        self.assertEqual(full, spawn(full, random.Random(1), count=4))


class TerminalTest(unittest.TestCase):

    def test_winning_value_is_detected(self):
        board = ((2048, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
        self.assertTrue(has_won(board))
        self.assertFalse(has_won(empty_board()))

    def test_an_empty_cell_leaves_a_move(self):
        self.assertTrue(has_moves(empty_board()))

    def test_a_full_checkerboard_has_no_moves(self):
        board = ((2, 4, 2, 4), (4, 2, 4, 2), (2, 4, 2, 4), (4, 2, 4, 2))
        self.assertFalse(has_moves(board))

    def test_a_full_board_with_an_equal_neighbour_still_moves(self):
        board = ((2, 2, 4, 8), (4, 8, 16, 32), (2, 4, 8, 16), (4, 8, 16, 32))
        self.assertTrue(has_moves(board))


if __name__ == "__main__":
    unittest.main()
