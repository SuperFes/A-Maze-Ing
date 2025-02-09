import random
import time

from cell import Cell

class Maze:
    def __init__(
            self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None
    ):
        random.seed(time.thread_time())

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        self._stack = []
        self._current = None
        self._solved = False

        self.__graph = dict()

        self.__create_cells()
        self.__draw_cells()

        self._break_entrance_and_exit()
        self._break_walls_r()

        self._reset_cells_visited()

        self._make_graph()

    def __create_cells(self):
        for i in range(self.__num_rows):
            self._cells.append([Cell(
                    self.__x1 + j * self.__cell_size_x,
                    self.__y1 + i * self.__cell_size_y,
                    self.__cell_size_x,
                    self.__cell_size_y,
                    self.__win,
                ) for j in range(self.__num_cols)])

    def __draw_cells(self):
        if self.__win is None:
            return

        for celly in self._cells:
            for cell in celly:
                cell.draw()

            self._animate(sleep_time=0.001)

    def _animate(self, sleep_time = 0.1):
        if self.__win is None:
            return

        self.__win.redraw()
        time.sleep(sleep_time)

    def _break_entrance_and_exit(self):
        self._cells[0][0].remove_wall(Cell.Wall.Top)
        self._cells[0][0].draw()
        self._animate()

        self._cells[-1][-1].remove_wall(Cell.Wall.Bottom)
        self._cells[-1][-1].draw()
        self._animate()

    def _break_walls_r(self):
        count = 0
        cells = self.__num_cols * self.__num_rows
        total = count / cells

        self._cells[0][0]._visited = True

        self._stack.append((0, 0))

        while len(self._stack) > 0:
            y, x = self._stack[-1]
            cell = self._cells[y][x]

            cell._visited = True

            neighbors = self._get_unvisited_neighbors((y, x))

            if len(neighbors) == 0:
                self._stack.pop()
                continue

            next_cell = random.choice(neighbors)
            self._remove_wall((y, x), next_cell)
            count += 1

            total = count / cells

            if total < 0.59:
                if count % 100 == 0:
                    self._animate(0.00000025)
            elif total < 0.69:
                if count % 50 == 0:
                    self._animate(0.00000025)
            elif total < 0.79:
                if count % 25 == 0:
                    self._animate(0.00000025)
            elif total < 0.89:
                if count % 10 == 0:
                    self._animate(0.00000025)
            elif total < 0.99:
                if count % 5 == 0:
                    self._animate(0.00000025)
            else:
                self._animate(0.00000025)

            self._stack.append(next_cell)

        self._animate(0.00000025)

    def _remove_wall(self, current, next_cell):
        y1, x1 = current
        y2, x2 = next_cell

        if x1 == x2:
            if y1 < y2:
                self._cells[y1][x1].remove_wall(Cell.Wall.Bottom)
                self._cells[y2][x2].remove_wall(Cell.Wall.Top)
            else:
                self._cells[y1][x1].remove_wall(Cell.Wall.Top)
                self._cells[y2][x2].remove_wall(Cell.Wall.Bottom)
        else:
            if x1 < x2:
                self._cells[y1][x1].remove_wall(Cell.Wall.Right)
                self._cells[y2][x2].remove_wall(Cell.Wall.Left)
            else:
                self._cells[y1][x1].remove_wall(Cell.Wall.Left)
                self._cells[y2][x2].remove_wall(Cell.Wall.Right)

        self._cells[y1][x1].draw()
        self._cells[y2][x2].draw()


    def _get_unvisited_neighbors(self, pos):
        y, x= pos

        neighbors = []

        if y > 0 and not self._cells[y - 1][x]._visited:
            neighbors.append((y - 1, x))

        if y < self.__num_rows - 1 and not self._cells[y + 1][x]._visited:
            neighbors.append((y + 1, x))

        if x > 0 and not self._cells[y][x - 1]._visited:
            neighbors.append((y, x - 1))

        if x < self.__num_cols - 1 and not self._cells[y][x + 1]._visited:
            neighbors.append((y, x + 1))

        return neighbors

    def _make_graph(self):
        for y in range(self.__num_rows):
            for x in range(self.__num_cols):
                node = f"{y}:{x}"

                if self.__graph.get(node, None) is None:
                    self.__graph[node] = []

                if not self._cells[y][x]._walls[Cell.Wall.Top] and y > 0:
                    self.__graph[node].append((y - 1, x))

                if not self._cells[y][x]._walls[Cell.Wall.Bottom] and y < self.__num_rows - 1:
                    self.__graph[node].append((y + 1, x))

                if not self._cells[y][x]._walls[Cell.Wall.Left] and x > 0:
                    self.__graph[node].append((y, x - 1))

                if not self._cells[y][x]._walls[Cell.Wall.Right] and x < self.__num_cols - 1:
                    self.__graph[node].append((y, x + 1))

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell._visited = False

    def solve(self):
        if self._solved:
            return self._solved

        start = "0:0"

        self._stack = [start]
        visited = set()

        while len(self._stack) > 0:
            popped = self._stack[-1]

            current = list(map(int, popped.split(":")))

            visited.add(popped)

            if current[0] == self.__num_rows - 1 and current[1] == self.__num_cols - 1:
                self._solved = True
                # return True

            neighbors = self.__graph[popped]
            unvisited_neighbors = []

            for n in neighbors:
                if f"{n[0]}:{n[1]}" not in visited:
                    unvisited_neighbors.append(f"{n[0]}:{n[1]}")

            if len(unvisited_neighbors) == 0:
                self._stack.pop()
                continue

            next_cell = random.choice(unvisited_neighbors)

            self._stack.append(next_cell)

            nn = list(map(int, next_cell.split(":")))

            self._cells[nn[0]][nn[1]].draw_move(self._cells[current[0]][current[1]])
            self._animate(0.0005)
