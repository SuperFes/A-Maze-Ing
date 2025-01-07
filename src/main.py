from window import Window
from maze import Maze

def main():
    win = Window(1024, 768)

    cell_size = 16
    cols = 1024 // cell_size - 1
    rows = 768 // cell_size - 1

    maze = Maze(8, 8, rows, cols, cell_size, cell_size, win)

    maze.solve()

    win.wait_for_close()

if __name__ == "__main__":
    main()
