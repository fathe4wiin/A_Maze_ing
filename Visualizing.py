import sys
from mlx import Mlx
from cell import Cell
from maze_solver import bfs
from maze_gen import MazeGen
from maze_algo import MazeAlgo

class MazeVisualizer:
    def __init__(self, maze, mlx_ptr=None, win=None, bg_color=0x55FFFFFF, cell_color=0xFFFFFFFF, wall_color=0xFF000000, pattern_color=0xFFFFD700, start=None, exit=None, perfect=False):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.start = start  # (x, y) tuple for start cell
        self.exit = exit    # (x, y) tuple for exit cell
        self.path = []      # List of cells in the solution path
        self.show_path = False  # Flag to control path visibility
        
        # Fixed window size, calculate tile size based on cells
        self.win_width = 1000
        self.win_height = 720
        self.tile_size = min(self.win_width // self.width, self.win_height // self.height)
        
        # Calculate offset to center the maze
        self.offset_x = (self.win_width - self.width * self.tile_size) // 2
        self.offset_y = (self.win_height - self.height * self.tile_size) // 2
        
        # Colors (from parameters)
        self.cell_color = cell_color
        self.wall_color = wall_color
        self.background_color = bg_color
        self.highlight_color = pattern_color

        self.mlx = Mlx()

        self.perfect = perfect
        if mlx_ptr:
            self.mlx_ptr = mlx_ptr
        else:
            self.mlx_ptr = self.mlx.mlx_init()
            
        if not self.mlx_ptr:
            print("Failed to initialize MLX")
            sys.exit(1)
        if win:
            self.win = win
        else:
            self.win = self.mlx.mlx_new_window(self.mlx_ptr, self.win_width, self.win_height, "Maze Visualizer")
        
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render_loop, None)
        self.mlx.mlx_mouse_hook(self.win, self.mouse_hook, None)
        
        # Initialize UI buttons once
        self.buttons = []
        self.setup_ui()
        
        # Precompute static 42 pattern
        self._compute_42_pattern()
        
        # Flag to track if maze needs redrawing
        self.needs_redraw = True

        # Clear background
        self.color_change(0, 0)
        
        # Draw the maze
        self.draw_maze()
        
        # Draw start/exit markers once
        marker_size = max(4, self.tile_size // 4)
        if self.start:
            sx, sy = self.start
            cell_center_x = self.offset_x + sx * self.tile_size + self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + sy * self.tile_size + self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, 0xFFFF0000)  # Red for start
        if self.exit:
            ex, ey = self.exit
            cell_center_x = self.offset_x + ex * self.tile_size + self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + ey * self.tile_size + self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, 0xFF00FF00)  # Green for exit

    def draw_pixel(self, x, y, color):
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

    def color_change(self, x, y):

        for x in range(self.win_width):
            for y in range (self.win_height):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, self.background_color)


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

    def draw_filled_rect(self, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.draw_pixel(i, j, color)

    def _compute_42_pattern(self):
        """Precompute the 42 pattern cells - called once."""
        four = [
            (0,0), (0,1), (0,2), # Left vertical
            (1,2),               # Middle horizontal
            (2,0), (2,1), (2,2), (2,3), (2,4) # Right vertical
        ]
        two = [
            (4,0), (5,0), (6,0), # Top horizontal
            (6,1),               # Top right
            (4,2), (5,2), (6,2), # Middle horizontal
            (4,3),               # Bottom left
            (4,4), (5,4), (6,4)  # Bottom horizontal
        ]
        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2
        self.text_cells = set((x + offset_x, y + offset_y) for x, y in four + two)

    def setup_ui(self):
        """Create UI buttons once - not every frame."""
        from mlx_ui import Button
        
        button_color = 0xFF272727
        text_color = 0xFFFFFFFF
        
        btn_regenerate = Button(
            self.mlx, self.mlx_ptr, self.win,
            x=1020, y=502,
            w=250, h=50,
            color=button_color,
            text="Regenerate Maze",
            text_color=text_color,
            on_click=lambda: self.regen()
        )
        
        btn_toggle_path = Button(
            self.mlx, self.mlx_ptr, self.win,
            x=1020, y=582,
            w=250, h=50,
            color=button_color,
            text="Toggle Path",
            text_color=text_color,
            on_click=lambda: self.solve()
        )
        
        btn_quit = Button(
            self.mlx, self.mlx_ptr, self.win,
            x=1045, y=662,
            w=200, h=50,
            color=button_color,
            text="Quit",
            text_color=text_color,
            on_click=lambda: self.close_window()
        )
        
        self.buttons = [btn_regenerate, btn_toggle_path, btn_quit]

    def draw_maze(self):
        """Draw the maze - called when maze changes."""
        # Draw entire maze area with cell color
        maze_pixel_width = self.width * self.tile_size
        maze_pixel_height = self.height * self.tile_size
        self.draw_filled_rect(self.offset_x, self.offset_y, maze_pixel_width, maze_pixel_height, self.cell_color)

        # Draw 42 pattern highlights
        for row in self.maze:
            for cell in row:
                x = self.offset_x + cell.x * self.tile_size
                y = self.offset_y + cell.y * self.tile_size
                
                if (cell.x, cell.y) in self.text_cells:
                    self.draw_filled_rect(x, y, self.tile_size, self.tile_size, self.highlight_color)

        # Draw walls on top
        for row in self.maze:
            for cell in row:
                x = self.offset_x + cell.x * self.tile_size
                y = self.offset_y + cell.y * self.tile_size
                
                if cell.walls['N']:
                    self.draw_line(x, y, x + self.tile_size, y, self.wall_color)
                if cell.walls['S']:
                    self.draw_line(x, y + self.tile_size, x + self.tile_size, y + self.tile_size, self.wall_color)
                if cell.walls['E']:
                    self.draw_line(x + self.tile_size, y, x + self.tile_size, y + self.tile_size, self.wall_color)
                if cell.walls['W']:
                    self.draw_line(x, y, x, y + self.tile_size, self.wall_color)

    def render_loop(self, param):
        # Draw existing buttons (don't recreate them)
        for btn in self.buttons:
            btn.draw()
        return 0

    def key_hook(self, keycode, param):
        if keycode == 65307:  # ESC
            self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def mouse_hook(self, button, x, y, param):
        if button == 1:  # Left click
            for btn in self.buttons:
                btn.handle_click(x, y)
        return 0

    def close_window(self):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def run(self):
        self.mlx.mlx_loop(self.mlx_ptr)
    
    def solve(self):
        if not self.start or not self.exit:
            return
        marker_size = max(4, self.tile_size // 4)
        if self.show_path == True:
            # Clear the path by drawing over it with cell color
            for cell in self.path:
                cell_center_x = self.offset_x + cell.x * self.tile_size + self.tile_size // 2 - marker_size // 2
                cell_center_y = self.offset_y + cell.y * self.tile_size + self.tile_size // 2 - marker_size // 2
                self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, self.cell_color)
            self.show_path = False
            return
        start_cell = self.maze[self.start[1]][self.start[0]]
        exit_cell = self.maze[self.exit[1]][self.exit[0]]
        self.path = bfs(self.maze, start_cell, exit_cell)
        # Draw the path immediately
        for cell in self.path:
            cell_center_x = self.offset_x + cell.x * self.tile_size + self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + cell.y * self.tile_size + self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, 0xFF00FF00)  # Green
        self.show_path = True


    def regen(self):
        """Regenerate the maze with a new random layout."""
        maze_gen = MazeGen()
        layout = maze_gen.create_cell_layout(self.width, self.height)
        self.maze = maze_gen.generate_maze(layout, perfect=self.perfect)
        self.path = []
        self.show_path = False
        # Redraw the maze
        self.color_change(0, 0)
        self.draw_maze()
        # Redraw start/exit markers
        marker_size = max(4, self.tile_size // 4)
        if self.start:
            sx, sy = self.start
            cell_center_x = self.offset_x + sx * self.tile_size + self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + sy * self.tile_size + self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, 0xFFFF0000)
        if self.exit:
            ex, ey = self.exit
            cell_center_x = self.offset_x + ex * self.tile_size + self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + ey * self.tile_size + self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(cell_center_x, cell_center_y, marker_size, marker_size, 0xFF00FF00)
