import sys
from maze import Maze
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog='Maze',
        description='Pogram create maze and solve it'
        )
    parser.add_argument('methods', type=str, help='Choose one method in [bfs, dijkstra, all, mst]')
    parser.add_argument('--upload', type=str, help='Input dir for upload maze]')
    parser.add_argument('--save', type=str, help='Input dir for save maze]')
    args = parser.parse_args()
    MAZE = Maze()
    methods = ['bfs', 'dijkstra', 'all', 'mst']

    try:
        MAZE.upload(args.upload)
    except:
        MAZE.crate_map()

    if args.methods == 'bfs':
        MAZE.dfs()
    elif args.methods == 'dijkstra':
        MAZE.dijkstra()
    elif args.methods == 'mst':
        MAZE.mst()
        return
    else:
        MAZE.show_maze()
        print("----DFS----")
        MAZE.dfs()
        MAZE.show_path()
        print("----DIJKSTRA---")
        MAZE.dijkstra()
        MAZE.show_path()
        MAZE.mst()
        return
    MAZE.show_maze()
    MAZE.show_path()
    try:
        MAZE.save(args.save)
    except:
        pass


if __name__ == '__main__':
    main()
