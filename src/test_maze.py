import unittest
from maze import Maze


class TestMaze(unittest.TestCase):

    def setUp(self):
        self.maze = Maze()

    def test_size(self):
        self.assertEqual(self.maze.return_size(), (25, 15))

    def test_changed_size(self):
        self.maze = Maze(cols=10, rows=10)
        self.assertEqual(self.maze.return_size(), (10, 10))

    def test_upload(self):
        self.maze.upload('../data/maze3.txt')
        self.assertEqual(self.maze.grid, [[1, 1, 1, 1], [0, 0, 0, 0]])

    def test_create_map(self):
        self.maze = Maze(4, 4)
        self.maze.crate_map(per=0)
        self.assertEqual(self.maze.grid, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])


if __name__ == '__main__':
    unittest.main(argv=['', '-v'], defaultTest='TestMaze', exit=False)