import sys
import random
from mlx import Mlx
from lib.maze_gen import MazeGen
from lib.parsing import Config
from lib.gen_outputfile import generate_output_file
from lib.main_menu import MainMenu
from lib.Visualizing import MazeVisualizer
from lib.errors import MazeError


def main() -> None:
    try:
        fconfig = sys.argv[1]
    except Exception as e:
        print(f"Error: {e}")
        return

    try:
        config: Config = Config(fconfig)
    except MazeError as e:
        print(f"Error: {e}")
        return

    random.seed(config.SEED)

    mazeGen = MazeGen()
    layout = mazeGen.create_cell_layout(config.WIDTH, config.HEIGHT)
    try:
        maze = mazeGen.generate_maze(layout, config)
    except MazeError as e:
        print(f"Error: {e}")
        return

    try:
        generate_output_file(
            maze,
            config.ENTRY,
            config.EXIT,
            config.OUTPUT_FILE)
    except MazeError as e:
        print(f"Error: {e}")
        return

    try:
        mlx = Mlx()
        if not mlx:
            raise MazeError("Failed to initialize MLX library")

        mlx_ptr = mlx.mlx_init()
        if not mlx_ptr:
            raise MazeError("Failed to initialize MLX: mlx_ptr is None")

        win = mlx.mlx_new_window(mlx_ptr, 1280, 720, "A-MAZE-ING")
        if not win:
            raise MazeError("Failed to create MLX window")

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

        menu.viz = viz
        viz.menu = menu
        menu.running = True

        while menu.running or viz.running:
            if menu.running:
                menu.run()
            elif viz.running:
                viz.run()

    except MazeError as e:
        print(f"MLX Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()
