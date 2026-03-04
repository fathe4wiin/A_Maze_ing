import sys
import random
from mlx import Mlx
from lib.maze_gen import MazeGen
from lib.parsing import Config
from lib.gen_outputfile import generate_output_file
from lib.main_menu import MainMenu
from lib.Visualizing import MazeVisualizer

def main():
    config: Config = Config("config.txt")
    random.seed(config.SEED)

    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    maze = maze.generate_maze(layout, config)

    if not maze:
        print("error")
        return
    generate_output_file(maze, config.ENTRY, config.EXIT, config.OUTPUT_FILE)

    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win = mlx.mlx_new_window(mlx_ptr, 1280, 720, "A-MAZE-ING")

    menu = MainMenu(maze, config, mlx=mlx, mlx_ptr=mlx_ptr, win=win)

    viz = MazeVisualizer(
            maze,
            mlx=mlx,
            mlx_ptr=mlx_ptr,
            win=win,
            player_color=menu.selected_colors['player'],
            cell_color=menu.selected_colors['cell'],
            wall_color=menu.selected_colors['wall'],
            pattern_color=menu.selected_colors['pattern'],
            config=config,
        )
    
    # Link menu and viz together
    menu.viz = viz
    viz.menu = menu
    menu.running = True

    while menu.running or viz.running:
        if menu.running:
            menu.run()
        elif viz.running:
            viz.run()


if __name__ == "__main__":
    main()