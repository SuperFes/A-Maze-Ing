from window import Window
from maze import Maze

def main():
    width = 1980
    height = 1080

    win = Window(width, height)

    cell_size = 8
    cols = (width // cell_size) - 1
    rows = (height // cell_size) - 1

    maze = Maze(cell_size // 2, cell_size // 2, rows, cols, cell_size, cell_size, win)

    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
