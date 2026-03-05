import sys
from mlx import Mlx
from .mlx_ui import Button, Label
from .cell import Cell
from .maze_solver import bfs
from .maze_gen import MazeGen
from .player import Player
from .stats import Stats
from .errors import MazeError
from typing import Any


class MazeVisualizer:
    def __init__(self,
                 maze: list[list[Cell]],
                 mlx: Mlx | None = None,
                 mlx_ptr: int | None = None,
                 win: int | None = None,
                 player_color: int = 0x55FFFFFF,
                 cell_color: int = 0xFFFFFFFF,
                 wall_color: int = 0xFF000000,
                 pattern_color: int = 0xFFFFD700,
                 config: Any = None,
                 menu: Any = None) -> None:
        self.running = False
        self.menu = menu
        self.maze = maze
        self.height = config.HEIGHT
        self.width = config.WIDTH
        self.config = config
        self.start = config.ENTRY
        self.exit = config.EXIT
        self.path: list[Cell] = []
        self.show_path = False

        self.win_width = 1000
        self.win_height = 720
        self.tile_size = min(
            self.win_width // self.width,
            self.win_height // self.height)

        self.offset_x = (self.win_width - self.width * self.tile_size) // 2
        self.offset_y = (self.win_height - self.height * self.tile_size) // 2

        self.cell_color = cell_color
        self.wall_color = wall_color
        self.player_color = player_color
        self.background_color = 0xFF7D7D7D
        self.highlight_color = pattern_color

        if mlx:
            self.mlx = mlx
        else:
            self.mlx = Mlx()

        self.perfect = config.PERFECT
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
            self.win = self.mlx.mlx_new_window(
                self.mlx_ptr,
                self.win_width,
                self.win_height,
                "Maze Visualizer"
            )

        self.player = Player(
            self.mlx,
            self.mlx_ptr,
            self.win,
            self.start[0],
            self.start[1],
            self.cell_color,
            self.maze,
            self.tile_size,
            self.offset_x,
            self.offset_y,
            player_color=player_color,
            start=self.start,
            exit=self.exit)
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render_loop, None)
        self.mlx.mlx_mouse_hook(self.win, self.mouse_hook, None)
        self.mlx.mlx_hook(self.win, 33, 0, self._close_hook, None)

        self.stats = Stats()

        self.buttons: list[Button] = []
        self.setup_ui()

        self.patt = config.pattern
        if self.patt:
            self._compute_42_pattern()
        else:
            self.text_cells: set[tuple[int, int]] = set()

        self.color_change(0, 0)

        self.draw_maze()

    def draw_start_exit(self) -> None:
        marker_size = max(4, self.tile_size // 4)
        if self.start:
            sx, sy = self.start
            cell_center_x = self.offset_x + sx * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + sy * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(
                cell_center_x,
                cell_center_y,
                marker_size,
                marker_size,
                0xFFFF0000)
        if self.exit:
            ex, ey = self.exit
            cell_center_x = self.offset_x + ex * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + ey * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(
                cell_center_x,
                cell_center_y,
                marker_size,
                marker_size,
                0xFF00FF00)

    def draw_pixel(self, x: int, y: int, color: int) -> None:
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

    def color_change(self, x: int, y: int) -> None:
        for x in range(self.win_width):
            for y in range(self.win_height):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr, self.win, x, y, self.background_color)

    def draw_line(
            self,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            color: int) -> None:
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

    def draw_filled_rect(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            color: int) -> None:
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.draw_pixel(i, j, color)

    def get_dark_color(self, color: int) -> int:
        """Return the lightened version of a color using simple ifs."""
        if color == 0xFF2196F3:
            return 0xFF90CAF9
        if color == 0xFFE53935:
            return 0xFFEF9A9A
        if color == 0xFFFB8C00:
            return 0xFFFFCC80
        if color == 0xFF43A047:
            return 0xFFA5D6A7
        if color == 0xFF8E24AA:
            return 0xFFCE93D8
        if color == 0xFF00BCD4:
            return 0xFF80DEEA
        if color == 0xFFFF4081:
            return 0xFFFF80AB
        if color == 0xFFFFD700:
            return 0xFFFFE57F
        if color == 0xFF00FF00:
            return 0xFF90EE90
        if color == 0xFF87CEEB:
            return 0xFFB0E0E6
        if color == 0xFF673AB7:
            return 0xFFB39DDB
        if color == 0xFFFF9800:
            return 0xFFFFCC80
        return 0xFFCFCFCF

    def _compute_42_pattern(self) -> None:
        """Precompute the 42 pattern cells - called once."""
        four = [
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)
        ]
        two = [
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]
        offset_x = (self.width - 7) // 2
        offset_y = (self.height - 5) // 2
        self.text_cells = set((x + offset_x, y + offset_y)
                              for x, y in four + two)

    def setup_ui(self) -> None:
        """Create UI buttons once - not every frame."""

        button_color = 0xFF272727
        text_color = 0xFFFFFFFF

        btn_regenerate = Button(
            self.mlx, self.mlx_ptr, self.win,
            x=1020, y=502,
            w=250, h=50,
            color=button_color,
            text="Reset & Regenerate",
            text_color=text_color,
            on_click=lambda: self.clear_score_and_player()
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
            text="Back to Menu",
            text_color=text_color,
            on_click=lambda: self._back_to_menu()
        )

        self.buttons = [btn_regenerate, btn_toggle_path, btn_quit]

        self.lbls = [
            Label(
                self.mlx,
                self.mlx_ptr,
                self.win,
                1040,
                12,
                "Mazes Solved:",
                0xFF000000),
            Label(
                self.mlx,
                self.mlx_ptr,
                self.win,
                1040,
                42,
                "Moves:",
                0xFF000000)]

        for lbl in self.lbls:
            lbl.draw()

        self.mazes_score = Label(
            self.mlx, self.mlx_ptr, self.win, 1200, 12, f"{
                self.stats.mazes_solved}", 0xFF000000)
        self.mazes_score.draw()

        self.steps = Label(
            self.mlx, self.mlx_ptr, self.win, 1200, 42, f"{
                self.stats.steps}", 0xFF000000)
        self.steps.draw()

    def draw_maze(self) -> None:
        """Draw the maze - called when maze changes."""
        for row in self.maze:
            for cell in row:
                x = self.offset_x + cell.x * self.tile_size
                y = self.offset_y + cell.y * self.tile_size

                if (cell.x, cell.y) in self.text_cells:
                    cell.color = self.highlight_color
                    cell.dark_color = self.get_dark_color(self.highlight_color)
                else:
                    cell.color = self.cell_color
                    cell.dark_color = self.get_dark_color(self.cell_color)
                cell.in_path = False

                self.draw_filled_rect(
                    x, y, self.tile_size, self.tile_size, cell.color)

        for row in self.maze:
            for cell in row:
                x = self.offset_x + cell.x * self.tile_size
                y = self.offset_y + cell.y * self.tile_size

                if cell.walls['N']:
                    self.draw_line(
                        x, y, x + self.tile_size, y, self.wall_color)
                if cell.walls['S']:
                    self.draw_line(
                        x,
                        y + self.tile_size,
                        x + self.tile_size,
                        y + self.tile_size,
                        self.wall_color)
                if cell.walls['E']:
                    self.draw_line(
                        x + self.tile_size,
                        y,
                        x + self.tile_size,
                        y + self.tile_size,
                        self.wall_color)
                if cell.walls['W']:
                    self.draw_line(
                        x, y, x, y + self.tile_size, self.wall_color)

        self.draw_start_exit()

    def render_loop(self, param: Any) -> int:
        if self.player.x == self.exit[0] and self.player.y == self.exit[1]:
            self.player_reset()

        for btn in self.buttons:
            btn.draw()

        if self.show_path:
            self.draw_path()

        self.player.draw()
        return 0

    def draw_path(self) -> None:
        """Draw the solution path by darkening the cells."""
        for cell in self.path:
            x = self.offset_x + cell.x * self.tile_size
            y = self.offset_y + cell.y * self.tile_size
            cell.in_path = True
            self.draw_filled_rect(
                x,
                y,
                self.tile_size,
                self.tile_size,
                cell.dark_color)

        for cell in self.path:
            x = self.offset_x + cell.x * self.tile_size
            y = self.offset_y + cell.y * self.tile_size
            if cell.walls['N']:
                self.draw_line(x, y, x + self.tile_size, y, self.wall_color)
            if cell.walls['S']:
                self.draw_line(
                    x,
                    y + self.tile_size,
                    x + self.tile_size,
                    y + self.tile_size,
                    self.wall_color)
            if cell.walls['E']:
                self.draw_line(
                    x + self.tile_size,
                    y,
                    x + self.tile_size,
                    y + self.tile_size,
                    self.wall_color)
            if cell.walls['W']:
                self.draw_line(x, y, x, y + self.tile_size, self.wall_color)

        self.draw_start_exit()

    def key_hook(self, keycode: int, param: Any) -> int:
        w = 119
        a = 97
        s = 115
        d = 100
        esc = 65307

        if keycode == esc:
            self._back_to_menu()
        elif keycode == w:
            if self.player.move("up"):
                self.stats.add_step()
                self.steps.update(0xFFD9D9D9, text=f"{self.stats.steps}")
        elif keycode == a:
            if self.player.move("left"):
                self.stats.add_step()
                self.steps.update(0xFFD9D9D9, text=f"{self.stats.steps}")
        elif keycode == s:
            if self.player.move("down"):
                self.stats.add_step()
                self.steps.update(0xFFD9D9D9, text=f"{self.stats.steps}")
        elif keycode == d:
            if self.player.move("right"):
                self.stats.add_step()
                self.steps.update(0xFFD9D9D9, text=f"{self.stats.steps}")
        return 0

    def _back_to_menu(self) -> None:
        """Go back to menu."""
        self.running = False
        if self.menu:
            self.menu.running = True
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def mouse_hook(self, button: int, x: int, y: int, param: Any) -> int:
        if button == 1:
            for btn in self.buttons:
                btn.handle_click(x, y)
        return 0

    def close_window(self) -> int:
        self.running = False
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def _close_hook(self, _: Any) -> int:
        """Window close event handler (event 33) - quits everything."""
        self.running = False
        if self.menu:
            self.menu.running = False
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def _setup_hooks(self) -> None:
        """Set up input hooks for the visualizer."""
        self.mlx.mlx_key_hook(self.win, self.key_hook, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.render_loop, None)
        self.mlx.mlx_mouse_hook(self.win, self.mouse_hook, None)
        self.mlx.mlx_hook(self.win, 33, 0, self._close_hook, None)

    def run(self) -> None:
        self.running = True

        self._setup_hooks()

        self.draw_maze()
        self.setup_ui()
        self.mlx.mlx_loop(self.mlx_ptr)

    def solve(self) -> None:
        if not self.start or not self.exit:
            return

        if self.show_path:
            for cell in self.path:
                cell.in_path = False
            self.show_path = False
            self.draw_maze()
            return

        start_cell = self.maze[self.start[1]][self.start[0]]
        exit_cell = self.maze[self.exit[1]][self.exit[0]]
        path_result = bfs(self.maze, start_cell, exit_cell)
        if not path_result:
            raise MazeError("No Path was found")
        self.path = path_result
        self.show_path = True

    def regen(self) -> None:
        """Regenerate the maze with a new random layout."""
        maze_gen = MazeGen()
        layout = maze_gen.create_cell_layout(self.width, self.height)
        self.maze = maze_gen.generate_maze(layout, self.config)
        self.path = []
        self.show_path = False

        self.color_change(0, 0)
        self.draw_maze()

        marker_size = max(4, self.tile_size // 4)
        if self.start:
            sx, sy = self.start
            cell_center_x = self.offset_x + sx * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + sy * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(
                cell_center_x,
                cell_center_y,
                marker_size,
                marker_size,
                0xFFFF0000)
        if self.exit:
            ex, ey = self.exit
            cell_center_x = self.offset_x + ex * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            cell_center_y = self.offset_y + ey * self.tile_size + \
                self.tile_size // 2 - marker_size // 2
            self.draw_filled_rect(
                cell_center_x,
                cell_center_y,
                marker_size,
                marker_size,
                0xFF00FF00)
        self.player.x = self.start[0]
        self.player.y = self.start[1]
        self.player.maze = self.maze

    def player_reset(self) -> None:
        self.regen()
        self.stats.add_maze()
        self.mazes_score.update(0xFFD9D9D9, text=f"{self.stats.mazes_solved}")
        self.steps.update(0xFFD9D9D9, text=f"{self.stats.steps}")
        self.steps.draw()
        self.mazes_score.draw()

    def score_clear(self) -> None:
        self.stats.mazes_solved = 0
        self.stats.steps = 0
        self.mazes_score.update(0xFFD9D9D9, f"{self.stats.mazes_solved}")
        self.steps.update(0xFFD9D9D9, f"{self.stats.steps}")

    def clear_score_and_player(self) -> None:
        self.player_reset()
        self.score_clear()