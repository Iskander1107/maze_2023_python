import sys
from maze import Maze


def main():
    args = sys.argv
    maze = Maze()
    methods = ['bfs', 'dijkstra', 'both']
    if len(args) < 2 or args[1] not in methods:
        print('Вы не ввели метод решения или ввели некорректно')
        return
    try:
        maze.upload(args[2])
    except:
        maze.crate_map()

    if args[1] == 'bfs':
        maze.dfs()
    elif args[1] == 'dijkstra':
        maze.dijkstra()
    else:
        maze.show_maze()
        print("----DFS----")
        maze.dfs()
        maze.show_path()
        print("----DIJKSTRA---")
        maze.dijkstra()
        maze.show_path()
        return
    maze.show_maze()
    maze.show_path()
    try:
        a.save(args[3])
    except:
        pass


if __name__ == '__main__':
    main()
