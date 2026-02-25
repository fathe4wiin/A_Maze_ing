from cell import Cell


class Player:
    def __init__(self, mlx, mlx_ptr, win, x, y, cell_color, maze:list[list[Cell]], tile_size=64, offset_x=0, offset_y=0, color=0xFF8000ff):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win = win
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = color
        self.radius = tile_size // 3
        self.cell_color = cell_color
        self.maze = maze

    def draw(self):
        """Draw the player as a circle."""
        # Calculate center of the tile
        center_x = self.offset_x + self.x * self.tile_size + self.tile_size // 2
        center_y = self.offset_y + self.y * self.tile_size + self.tile_size // 2
        
        # Draw filled circle using midpoint circle algorithm
        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                if dx * dx + dy * dy <= self.radius * self.radius:
                    self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, center_x + dx, center_y + dy, self.color)

    def move(self, direction):
        rows = len(self.maze)
        cols = len(self.maze[0]) if rows > 0 else 0

        self.clear()
        if direction == 'up' and self.y > 0 and self.can_move(self.maze[self.y][self.x], self.maze[self.y - 1][self.x]):
            self.y -= 1
        elif direction == 'down' and self.y < rows - 1 and self.can_move(self.maze[self.y][self.x], self.maze[self.y + 1][self.x]):
            self.y += 1
        elif direction == 'left' and self.x > 0 and self.can_move(self.maze[self.y][self.x], self.maze[self.y][self.x - 1]):
            self.x -= 1
        elif direction == 'right' and self.x < cols - 1 and self.can_move(self.maze[self.y][self.x], self.maze[self.y][self.x + 1]):
            self.x += 1

        self.draw()
    def cleanup(self):
        """Clean up resources (no longer needed for circle drawing)."""
        pass

    def clear(self):
        center_x = self.offset_x + self.x * self.tile_size + self.tile_size // 2
        center_y = self.offset_y + self.y * self.tile_size + self.tile_size // 2
        
        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                if dx * dx + dy * dy <= self.radius * self.radius:
                    self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, center_x + dx, center_y + dy, self.cell_color)

    def can_move(self, current: Cell, dest: Cell):
        if not current or not dest:
            return False
        return current.is_accessible(dest)
