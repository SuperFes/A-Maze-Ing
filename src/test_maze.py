import unittest

from maze import Maze

class MazeTests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_rows,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_cols,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_entrance_and_exit()
        self.assertTrue(m1._cells[0][0].is_open)
        self.assertTrue(m1._cells[num_rows-1][num_cols-1].is_open)

    def test_maze_break_walls_r(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._break_walls_r()
        for row in m1._cells:
            for cell in row:
                self.assertTrue(cell.is_open)

    def test_maze_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._reset_cells_visited()
        for row in m1._cells:
            for cell in row:
                self.assertFalse(cell._visited)

if __name__ == "__main__":
    unittest.main()
