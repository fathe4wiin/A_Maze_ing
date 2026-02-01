import sys
from maze_gen import MazeGen
from parsing import Config

def main():
    config = Config("config.txt")
    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    



if __name__ == "__main__":
    main()