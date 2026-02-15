import sys
from mlx import Mlx

class MazeVisualizer:
    def __init__(self, maze, generator=None, tile_size=20):
        self.maze = maze
        self.generator = generator
        self.height = len(maze)
        self.width = len(maze[0])
        self.tile_size = tile_size
        self.win_width = self.width * self.tile_size
        self.win_height = self.height * self.tile_size

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()
        if not self.mlx_ptr:
            print("Failed to initialize MLX")
            sys.exit(1)
        
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, self.win_width, self.win_height, "Maze Visualizer")
        
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render_loop, None)

    def draw_pixel(self, x, y, color):
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

    def color_change(self, x, y):
        background_color = 0xFFFFFFFF # White
        for x in range(self.win_width):
            for y in range (self.win_height):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, background_color)


    def draw_line(self, x1, y1, x2, y2, color):
        # Implementation of Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.draw_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy


    def render_loop(self, param):
        if self.generator:
            try:
                self.maze = next(self.generator)
            except StopIteration:
                self.generator = None

        # Clear and Draw
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win)
        
        for row in self.maze:
            for cell in row:
                x = cell.x * self.tile_size
                y = cell.y * self.tile_size
                
                # Highlight current/visited if we wanted to
                wall_color = 0x00000000 # Black
                
                if cell.walls['N']:
                    self.draw_line(x, y, x + self.tile_size, y, wall_color)
                if cell.walls['S']:
                    self.draw_line(x, y + self.tile_size, x + self.tile_size, y + self.tile_size, wall_color)
                if cell.walls['E']:
                    self.draw_line(x + self.tile_size, y, x + self.tile_size, y + self.tile_size, wall_color)
                if cell.walls['W']:
                    self.draw_line(x, y, x, y + self.tile_size, wall_color)
        
        return 0

    def key_hook(self, keycode, param):
        if keycode == 65307: # ESC
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def run(self):
        self.mlx.mlx_loop(self.mlx_ptr)
