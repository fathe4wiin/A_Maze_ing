import sys
from maze_gen import MazeGen
from parsing import Config
from Visualizing import MazeVisualizer

def main():
    config: Config = Config("config.txt")
    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    gen = maze.generate_maze(layout, config.PERFECT)
    
    viz = MazeVisualizer(layout, generator=gen)
    viz.run()
    



if __name__ == "__main__":
    main()