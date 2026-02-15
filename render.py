import sys
from mlx import Mlx

def main():
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    if not mlx_ptr:
        print("Failed to init MLX")
        return

    width, height = 800, 600
    win = mlx.mlx_new_window(mlx_ptr, width, height, "Pixel Put Demo")
    blue_color = 0x00FFFFFF



    mlx.mlx_loop_hook(mlx_ptr, render_loop, None)
    mlx.mlx_key_hook(win, key_hook, None)

    mlx.mlx_loop(mlx_ptr)

class MazeVisualizer:
    def __init__(self, maze):
        self.width = 800
        self.height = 600
        self.maze = maze
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, self.width, self.height, "Pixel Put Demo")
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render_loop, None)
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)

        self.mlx.mlx_loop(self.mlx_ptr)

    def render_loop(self, param):
        for y in range(self.height):
            for x in range(self.width):
                self.put_

    def key_hook(self, keycode, param):
        print(f"Key pressed: {keycode}")
        if keycode == 65307: # ESC
            self.mlx.mlx_loop_exit(self.mlx_ptr)
    