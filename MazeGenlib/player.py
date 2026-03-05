from .cell import Cell
from mlx import Mlx


class Player:
    def __init__(
            self,
            mlx: Mlx,
            mlx_ptr: int,
            win: int,
            x: int,
            y: int,
            cell_color: int,
            maze: list[list[Cell]],
            tile_size: int = 64,
            offset_x: int = 0,
            offset_y: int = 0,
            player_color: int = 0xFF8000ff,
            start: tuple[int, int] | None = None,
            exit: tuple[int, int] | None = None
            ) -> None:
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win = win
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.color = player_color
        self.radius = tile_size // 3
        self.cell_color = cell_color
        self.maze = maze
        self.start = start
        self.exit = exit

    def draw(self) -> None:
        """Draw the player as a circle."""

        center_x = (
            self.offset_x +
            self.x * self.tile_size +
            self.tile_size // 2
            )
        center_y = (
            self.offset_y +
            self.y * self.tile_size +
            self.tile_size // 2
            )

        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                if dx * dx + dy * dy <= self.radius * self.radius:
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr,
                        self.win,
                        center_x + dx,
                        center_y + dy,
                        self.color)

    def move(self, direction: str) -> bool:
        rows = len(self.maze)
        cols = len(self.maze[0]) if rows > 0 else 0

        if direction == 'up' and self.y > 0 and self.can_move(
                self.maze[self.y][self.x], self.maze[self.y - 1][self.x]):
            self.clear()
            self.y -= 1
            self.draw()
            return True
        elif direction == 'down' and self.y < rows - 1 and self.can_move(
                self.maze[self.y][self.x], self.maze[self.y + 1][self.x]):
            self.clear()
            self.y += 1
            self.draw()
            return True
        elif direction == 'left' and self.x > 0 and self.can_move(
                self.maze[self.y][self.x], self.maze[self.y][self.x - 1]):
            self.clear()
            self.x -= 1
            self.draw()
            return True
        elif direction == 'right' and self.x < cols - 1 and self.can_move(
                self.maze[self.y][self.x], self.maze[self.y][self.x + 1]):
            self.clear()
            self.x += 1
            self.draw()
            return True

        return False

    def clear(self) -> None:
        center_x = (
            self.offset_x +
            self.x * self.tile_size +
            self.tile_size // 2
            )
        center_y = (
            self.offset_y +
            self.y * self.tile_size +
            self.tile_size // 2
            )

        cell = self.maze[self.y][self.x]
        if cell.in_path:
            cell_color = cell.dark_color
        else:
            cell_color = cell.color

        for dy in range(-self.radius, self.radius + 1):
            for dx in range(-self.radius, self.radius + 1):
                if dx * dx + dy * dy <= self.radius * self.radius:
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr,
                        self.win,
                        center_x + dx,
                        center_y + dy,
                        cell_color)

        marker_size = max(4, self.tile_size // 4)
        if self.start and (self.x, self.y) == self.start:
            mx = center_x - marker_size // 2
            my = center_y - marker_size // 2
            for i in range(marker_size):
                for j in range(marker_size):
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr, self.win, mx + i, my + j, 0xFFFF0000)
        if self.exit and (self.x, self.y) == self.exit:
            mx = center_x - marker_size // 2
            my = center_y - marker_size // 2
            for i in range(marker_size):
                for j in range(marker_size):
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr, self.win, mx + i, my + j, 0xFF00FF00)

    def can_move(self, current: Cell | None, dest: Cell | None) -> bool:
        if not current or not dest:
            return False
        return current.is_accessible(dest)

