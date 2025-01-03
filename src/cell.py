from enum import IntEnum

from line import Line
from point import Point

class Cell:
    class Wall(IntEnum):
        Left = 0,
        Top = 1,
        Right = 2,
        Bottom = 3,

    def __init__(self, x, y, width, height, win=None):
        self._walls = [True, True, True, True]
        self._visited = False
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.__win = win
        self.is_open = False

    def draw(self, fill_color = "black"):
        if self.__win is None:
            return

        x = self._x
        y = self._y
        x1 = x + self._width
        y1 = y + self._height

        if self._walls[Cell.Wall.Left]:
            self.__win.draw_line(Line(Point(x, y), Point(x, y1)), fill_color)
        else:
            self.__win.draw_line(Line(Point(x, y), Point(x, y1)), "#ffffff")

        if self._walls[Cell.Wall.Top]:
            self.__win.draw_line(Line(Point(x, y), Point(x1, y)), fill_color)
        else:
            self.__win.draw_line(Line(Point(x, y), Point(x1, y)), "#ffffff")

        if self._walls[Cell.Wall.Right]:
            self.__win.draw_line(Line(Point(x1, y), Point(x1, y1)), fill_color)
        else:
            self.__win.draw_line(Line(Point(x1, y), Point(x1, y1)), "#ffffff")

        if self._walls[Cell.Wall.Bottom]:
            self.__win.draw_line(Line(Point(x, y1), Point(x1, y1)), fill_color)
        else:
            self.__win.draw_line(Line(Point(x, y1), Point(x1, y1)), "#ffffff")

    def remove_wall(self, wall):
        if not self.is_open:
            self.is_open = True

        self._walls[wall] = False

    def draw_move(self, to_cell, undo=False):
        if self.__win is None:
            return

        x = self._x + self._width // 2
        y = self._y + self._height // 2

        dx = to_cell._x + to_cell._width // 2 - x
        dy = to_cell._y + to_cell._height // 2 - y

        if undo:
            self.__win.draw_line(Line(Point(x, y), Point(x + dx, y + dy)), "red")
        else:
            self.__win.draw_line(Line(Point(x, y), Point(x + dx, y + dy)), "green")
            self._visited = True
