from mlx import Mlx
from .mlx_ui import Button
from .parsing import Config
from typing import Any


class MainMenu:
    def __init__(
            self,
            maze: list,
            config: Config,
            mlx: Mlx | None = None,
            mlx_ptr: int | None = None,
            win: int | None = None) -> None:
        self.running = False
        self.viz: Any = None
        self.maze = maze
        self.config = config
        self.pattern = config.pattern

        # Window dimensions
        self.win_width = 1280
        self.win_height = 720

        self.selected_colors = {
            'player': 0xFFFF2D95,
            'cell': 0xFF2196F3,
            'wall': 0xFF000000,
            'pattern': 0xFFFF4081
        }

        self.menu_ui: list[Button] = []
        self.bg_ui: list[Button] = []
        self.cell_ui: list[Button] = []
        self.wall_ui: list[Button] = []
        self.patt_ui: list[Button] = []

        if mlx:
            self.mlx = mlx
        else:
            self.mlx = Mlx()

        if mlx_ptr:
            self.mlx_ptr = mlx_ptr
        else:
            self.mlx_ptr = self.mlx.mlx_init()

        if win:
            self.win = win
        else:
            self.win = self.mlx.mlx_new_window(
                self.mlx_ptr, self.win_width, self.win_height,
                "Maze Generator")

        self._create_menu_buttons()
        self._create_bg_color_buttons()
        self._create_cell_color_buttons()
        self._create_wall_color_buttons()
        self._create_pattern_color_buttons()

    def _draw_pixel(self, x: int, y: int, color: int) -> None:
        """Draw a single pixel."""
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

    def _draw_filled_rect(
            self,
            x: int,
            y: int,
            width: int,
            height: int,
            color: int) -> None:
        """Draw a filled rectangle."""
        for i in range(x, x + width):
            for j in range(y, y + height):
                self._draw_pixel(i, j, color)

    def _draw_background(self) -> None:
        """Draw the menu background."""
        self._draw_filled_rect(0, 0, 1000, 720, 0xFF7D7D7D)
        self._draw_filled_rect(1000, 0, 280, 720, 0xFFD9D9D9)

    def _set_color(self, color: int, key: str):  # type: ignore[no-untyped-def]
        """Create a setter function for a color."""
        def setter() -> None:
            self.selected_colors[key] = color
            self._draw_menu()
        return setter

    def _create_menu_buttons(self) -> None:
        """Create the main menu buttons."""
        self.menu_ui = [
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                304,
                208,
                150,
                50,
                0xff272727,
                "Player Color",
                text_color=0xFFFFFFFF),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                304,
                357,
                150,
                50,
                0xff272727,
                "Wall Color",
                text_color=0xFFFFFFFF),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                545,
                208,
                150,
                50,
                0xff272727,
                "Cell Color",
                text_color=0xFFFFFFFF),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                545,
                357,
                150,
                50,
                0xff272727,
                "42 Color",
                text_color=0xFFFFFFFF),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                380,
                141,
                250,
                50,
                0xff272727,
                "Generate Maze",
                text_color=0xffffff,
                on_click=lambda: self._start_viz()),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                400,
                530,
                200,
                50,
                0xff272727,
                "Quit",
                text_color=0xFFFFFFFF,
                on_click=lambda: self._quit_app())]

    def _create_bg_color_buttons(self) -> None:
        """Create color picker buttons for player."""
        self.bg_ui = [
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                304, 264, 30, 30, 0xFFFF2D95, "",
                on_click=self._set_color(0xFFFF2D95, "player")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                364, 264, 30, 30, 0xFF7C4DFF, "",
                on_click=self._set_color(0xFF7C4DFF, "player")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                424, 264, 30, 30, 0xFFFFB300, "",
                on_click=self._set_color(0xFFFFB300, "player")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                304, 299, 30, 30, 0xFFAEEA00, "",
                on_click=self._set_color(0xFFAEEA00, "player")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                364, 299, 30, 30, 0xFFFF6F61, "",
                on_click=self._set_color(0xFFFF6F61, "player")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win,
                424, 299, 30, 30, 0xFFF5F5F5, "",
                on_click=self._set_color(0xFFF5F5F5, "player")
                )
        ]

    def _create_cell_color_buttons(self) -> None:
        """Create color picker buttons for cells."""
        self.cell_ui = [
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 545, 264, 30, 30, 0xFF2196F3, "",
                on_click=self._set_color(0xFF2196F3, "cell")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 605, 264, 30, 30, 0xFFE53935, "",
                on_click=self._set_color(0xFFE53935, "cell")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 665, 264, 30, 30, 0xFFFB8C00, "",
                on_click=self._set_color(0xFFFB8C00, "cell")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 545, 299, 30, 30, 0xFF43A047, "",
                on_click=self._set_color(0xFF43A047, "cell")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 605, 299, 30, 30, 0xFF8E24AA, "",
                on_click=self._set_color(0xFF8E24AA, "cell")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 665, 299, 30, 30, 0xFF00BCD4, "",
                on_click=self._set_color(0xFF00BCD4, "cell")
                )
        ]

    def _create_wall_color_buttons(self) -> None:
        """Create color picker buttons for walls."""
        self.wall_ui = [
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 304, 413, 30, 30, 0xFF000000, "",
                on_click=self._set_color(0xFF000000, "wall")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 364, 413, 30, 30, 0xFFFFFFFF, "",
                on_click=self._set_color(0xFFFFFFFF, "wall")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 424, 413, 30, 30, 0xFF424242, "",
                on_click=self._set_color(0xFF424242, "wall")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 304, 448, 30, 30, 0xFFBDBDBD, "",
                on_click=self._set_color(0xFFBDBDBD, "wall")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 364, 448, 30, 30, 0xFF3F51B5, "",
                on_click=self._set_color(0xFF3F51B5, "wall")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 424, 448, 30, 30, 0xFF800000, "",
                on_click=self._set_color(0xFF800000, "wall")
                )
        ]

    def _create_pattern_color_buttons(self) -> None:
        """Create color picker buttons for pattern."""
        self.patt_ui = [
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 545, 413, 30, 30, 0xFFFF4081, "",
                on_click=self._set_color(0xFFFF4081, "pattern")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 605, 413, 30, 30, 0xFFFFD700, "",
                on_click=self._set_color(0xFFFFD700, "pattern")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 665, 413, 30, 30, 0xFF00FF00, "",
                on_click=self._set_color(0xFF00FF00, "pattern")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 545, 448, 30, 30, 0xFF87CEEB, "",
                on_click=self._set_color(0xFF87CEEB, "pattern")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 605, 448, 30, 30, 0xFF673AB7, "",
                on_click=self._set_color(0xFF673AB7, "pattern")
                ),
            Button(
                self.mlx,
                self.mlx_ptr,
                self.win, 665, 448, 30, 30, 0xFFFF9800, "",
                on_click=self._set_color(0xFFFF9800, "pattern")
                )
        ]

    def _get_all_buttons(self) -> list[Button]:
        """Return all button lists combined."""
        return (
            self.menu_ui +
            self.bg_ui +
            self.cell_ui +
            self.wall_ui +
            self.patt_ui
            )

    def _draw_menu(self) -> None:
        """Draw all menu elements -
            called once initially and when colors change."""
        for btn in self._get_all_buttons():
            btn.draw()

        self._draw_filled_rect(
            459, 208, 18, 50, self.selected_colors['player'])
        self._draw_filled_rect(700, 208, 18, 50, self.selected_colors['cell'])
        self._draw_filled_rect(459, 357, 18, 50, self.selected_colors['wall'])
        self._draw_filled_rect(
            700, 357, 18, 50, self.selected_colors['pattern'])

    def _render_loop(self, _: Any) -> None:
        """Render loop callback."""
        pass

    def _mouse_hook(self, button: int, x: int, y: int, _: Any) -> int:
        """Mouse click handler."""
        if button == 1:
            for btn in self._get_all_buttons():
                btn.handle_click(x, y)
        return 0

    def _key_hook(self, keycode: int, _: Any) -> int:
        """Key press handler."""
        if keycode == 65307:
            self._quit_app()
        return 0

    def _start_viz(self) -> None:
        """Stop menu loop to start visualizer."""
        self.running = False
        if self.viz:
            self.viz.player_color = self.selected_colors['player']
            self.viz.player.color = self.selected_colors['player']
            self.viz.cell_color = self.selected_colors['cell']
            self.viz.wall_color = self.selected_colors['wall']
            self.viz.highlight_color = self.selected_colors['pattern']
            self.viz.running = True
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _quit_app(self) -> None:
        """Quit the entire application."""
        self.running = False
        if self.viz:
            self.viz.running = False
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def _close_hook(self, _: Any) -> int:
        """Window close event handler (event 33)."""
        self._quit_app()
        return 0

    def _setup_hooks(self) -> None:
        """Set up input hooks for the menu."""
        self.mlx.mlx_key_hook(self.win, self._key_hook, None)
        self.mlx.mlx_loop_hook(self.mlx_ptr, self._render_loop, None)
        self.mlx.mlx_mouse_hook(self.win, self._mouse_hook, None)
        self.mlx.mlx_hook(self.win, 33, 0, self._close_hook, None)

    def run(self) -> None:
        """Run the menu once (draws and starts mlx loop)."""
        self.running = True

        self._setup_hooks()

        self._draw_background()
        self._draw_menu()
        self.mlx.mlx_loop(self.mlx_ptr)

    def quit(self) -> None:
        """Exit the main menu."""
        self._quit_app()
