from random import random, randint
from collections import deque
import heapq

class Maze:
    def __init__(self, cols=25, rows=15):
        self.map = None
        self.cols = cols
        self.rows = rows
        self.visited = None
        self.start = None
        self.end = None
        self.grid = None
        self.weights = None

    def crate_map(self, per=0.2):
        self.grid = [[1 if random() < per else 0 for col in range(self.cols)] for row in range(self.rows)]
        self.grid[0][0] = 0
        self.grid[self.rows - 1][self.cols - 1] = 0
        self.map = []
        for row in self.grid:
            self.map.append(['_' if col == 0 else '|' for col in row])

    def __get_next_node(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not self.grid[y][
            x] else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.__generate_weights(), (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def dfs(self, start=(0, 0), end=(0, 0)):
        if end == (0, 0):
            self.end = (self.cols - 1, self.rows - 1)
        else:
            self.end = end
        self.start = start
        queue = deque([self.start])

        self.visited = {self.start: None}
        cur_node = self.start
        graph = {}

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + [x[1] for x in self.__get_next_node(x, y)]

        while queue:
            cur_node = queue.popleft()
            if cur_node == self.end:
                break
            try:
                next_nodes = graph[cur_node]
            except KeyError:
                print('НАЧАЛА ЗАВАЛЕНО ЧЕМ-ТО')
                break
            for next_node in next_nodes:
                if next_node not in self.visited:
                    queue.append(next_node)
                    self.visited[next_node] = cur_node

    def __generate_weights(self):
        return randint(1, 10)

    def __clean_map(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.map[row][col] == '*':
                    self.map[row][col] = '_'

    def dijkstra(self, start=(0, 0), end=(0, 0)):

        if end == (0, 0):
            self.end = (self.cols - 1, self.rows - 1)
        else:
            self.end = end
        self.start = start

        queue = []
        heapq.heappush(queue, (0, self.start))
        self.visited = {self.start: None}
        graph = {}
        cost = {self.start: 0}

        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                graph[(x, y)] = graph.get((x, y), []) + self.__get_next_node(x, y)
        while queue:
            cur_cost, cur_node = heapq.heappop(queue)
            if cur_node == self.end:
                break

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost[cur_node] + neigh_cost

                if neigh_node not in cost or new_cost < cost[neigh_node]:
                    heapq.heappush(queue, (new_cost, neigh_node))
                    cost[neigh_node] = new_cost
                    self.visited[neigh_node] = cur_node

    def mst(self, start=(0, 0), end=(0, 0)):
        if end == (0, 0):
            self.end = (self.cols - 1, self.rows - 1)
        else:
            self.end = end
        self.start = start

        # инициализация
        unvisited = set((x, y) for y in range(self.rows) for x in range(self.cols) if self.grid[y][x] == 0)
        visited = set()
        edges = []
        total_weight = 0

        # выбор первой вершины
        cur_node = self.start
        visited.add(cur_node)
        unvisited.remove(cur_node)
        # добавление рёбер, пока все вершины не будут пройдены
        while unvisited:
            # получение всех соседних вершин, которые ещё не посещены
            neighbors = set()
            for node in visited:
                for neighbor in self.__get_next_node(node[0], node[1]):
                    if neighbor[1] in unvisited:
                        neighbors.add(neighbor[1])
            # получение ребра с минимальным весом
            min_weight, min_edge = float('inf'), None
            for edge in [(self.__generate_weights(), (node, neighbor)) for node in visited for neighbor in neighbors]:
                weight, _ = edge
                if weight < min_weight:
                    min_weight, min_edge = weight, edge
            # добавление найденного ребра в MST
            try:
                weight, (n1, n2) = min_edge
            except:
                print("ЧТО-то не так")
                return
            total_weight += weight
            edges.append(min_edge)
            # добавление вершины в посещённые
            visited.add(n2)
            unvisited.remove(n2)
            if self.end in visited:
                break
        print('----MST---')
        mst_map = self.map.copy()
        for node in visited:
            mst_map[node[1]][node[0]] = '*'
        for row in mst_map:
            print(*row)
    def show_path(self):
        solved_map = self.map.copy()
        print('----SHOW PATH----')
        cur_node = self.end
        # print(f'{cur_node} ', end='')
        while cur_node != self.start:
            try:
                cur_node = self.visited[cur_node]
            except KeyError:
                print('НЕТ ПУТИ')
                return
            # print(f'---> {cur_node} ', end='')
            solved_map[cur_node[1]][cur_node[0]] = '*'
        print()
        solved_map[self.end[1]][self.end[0]] = '*'
        for row in solved_map:
            print(*row)
        self.__clean_map()

    def save(self, filename):
        with open(filename, "w") as f:
            for s in self.grid:
                f.write(' '.join(str(elem) for elem in s) + '\n')

    def upload(self, filename):
        self.grid = []
        max_len = 0
        with open(filename, "r") as f:
            for line in f:
                tmp = list(map(lambda x: int(x), line.strip().split()))
                if len(tmp) > max_len:
                    max_len = len(tmp)
                self.grid.append(tmp)
        for row in range(len(self.grid)):
            if len(self.grid[row]) <= max_len:
                self.grid[row] += [1 for i in range(max_len - len(self.grid[row]))]
        print(self.grid)
        self.cols = max_len
        self.rows = len(self.grid)
        self.map = []
        for row in self.grid:
            self.map.append(['_' if col == 0 else '|' for col in row])
        self.__generate_weights()

    def show_maze(self):
        print('----PRINT MAZE----')
        for row in self.map:
            print(*row)

    def return_size(self):
        return (self.cols, self.rows)