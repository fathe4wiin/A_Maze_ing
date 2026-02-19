import sys
from maze_gen import MazeGen
from parsing import Config
from Visualizing import MazeVisualizer
from mlx_ui import Label, Button, Window
from mlx import Mlx

def main():


    config: Config = Config("config.txt")
    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    gen = maze.generate_maze(layout, config.PERFECT)

    def render_loop(_):
        btn.draw()

    def mouse_hook(button, x, y, _):
        if button == 1:
            if btn.is_clicked(x, y):
                print(f"dawda")
                btn.destroy()
                viz = MazeVisualizer(layout, mlx_ptr=win.mlx_ptr, win=win.win)
                viz.run()

    def key_hook(keycode, _):
        if keycode == 65307:  # ESC
            win.mlx.mlx_loop_exit(win.mlx_ptr)
        return 0
    
    win = Window(1280, 720, "Maze Generator", on_mouse=mouse_hook, on_loop=render_loop, on_key=key_hook)
    win.draw_filled_rect(0, 0, 1000, 720, 0xFF94AFFF)
    win.draw_filled_rect(1000, 0, 280, 720, 0xFF4755ff)
    btn = Button(win.mlx, win.mlx_ptr, win.win, 350, 200, 200, 50, 0xFF2525ae, "Generate Maze")
    
    win.mlx.mlx_loop(win.mlx_ptr)


if __name__ == "__main__":
    main()


