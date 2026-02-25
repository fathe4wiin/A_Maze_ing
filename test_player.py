from mlx import Mlx
from player import Player

# Initialize MLX
mlx = Mlx()
mlx_ptr = mlx.mlx_init()

# Create a window (800x600)
win = mlx.mlx_new_window(mlx_ptr, 800, 600, "Player Test")

# Create player at position (5, 5) with the goat image
player = Player(mlx, mlx_ptr, win, 5, 5, "assets/goat_rgba.png")

# Draw the player
player.draw()

# Start the event loop
mlx.mlx_loop(mlx_ptr)
