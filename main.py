import sys
from maze_gen import MazeGen
from parsing import Config
from Visualizing import MazeVisualizer
from mlx_ui import Label, Button, Window
from mlx import Mlx

def main():
    # Selected colors (will be passed to visualizer)
    selected_colors = {
        'bg': 0xFFFFFFFF,
        'cell': 0xFF2196F3,
        'wall': 0xFF000000,
        'pattern': 0xFFFF4081
    }

    def set_bg_color(color):
        def setter():
            selected_colors['bg'] = color
        return setter

    def set_cell_color(color):
        def setter():
            selected_colors['cell'] = color
        return setter

    def set_wall_color(color):
        def setter():
            selected_colors['wall'] = color
        return setter

    def set_pattern_color(color):
        def setter():
            selected_colors['pattern'] = color
        return setter

    config: Config = Config("config.txt")
    maze = MazeGen()
    layout = maze.create_cell_layout(config.WIDTH, config.HEIGHT)
    gen = maze.generate_maze(layout, config.PERFECT)

    def render_loop(_):
        start_btn.draw()
        bg_btn.draw()
        wall_btn.draw()
        cell_btn.draw()
        patt_btn.draw()
        quit_btn.draw()
        for btn in bg_colors + cell_colors + wall_colors + patt_colors:
            btn.draw()
        # Draw color preview rectangles next to each category button
        # BG preview (right side of bg_btn: x=304+150+5=459, y=208, 30x50)
        win.draw_filled_rect(459, 208, 18, 50, selected_colors['bg'])
        # Cell preview (right side of cell_btn: x=545+150+5=700, y=208, 30x50)
        win.draw_filled_rect(700, 208, 18, 50, selected_colors['cell'])
        # Wall preview (right side of wall_btn: x=304+150+5=459, y=357, 30x50)
        win.draw_filled_rect(459, 357, 18, 50, selected_colors['wall'])
        # Pattern preview (right side of patt_btn: x=545+150+5=700, y=357, 30x50)
        win.draw_filled_rect(700, 357, 18, 50, selected_colors['pattern'])

    def mouse_hook(button, x, y, _):
        if button == 1:
            if start_btn.is_clicked(x, y):
                start_btn.destroy()
                viz = MazeVisualizer(
                    layout,
                    mlx_ptr=win.mlx_ptr,
                    win=win.win,
                    bg_color=selected_colors['bg'],
                    cell_color=selected_colors['cell'],
                    wall_color=selected_colors['wall'],
                    pattern_color=selected_colors['pattern']
                )
                viz.run()
            if quit_btn.is_clicked(x, y):
                start_btn.destroy()
                win.mlx.mlx_loop_exit(win.mlx_ptr)
            # Handle color button clicks
            for btn in bg_colors + cell_colors + wall_colors + patt_colors:
                btn.handle_click(x, y)

    def key_hook(keycode, _):
        if keycode == 65307:  # ESC
            win.mlx.mlx_loop_exit(win.mlx_ptr)
        return 0
    
    win = Window(1280, 720, "Maze Generator", on_mouse=mouse_hook, on_loop=render_loop, on_key=key_hook)
    win.draw_filled_rect(0, 0, 1000, 720, 0xFF94AFFF)
    win.draw_filled_rect(1000, 0, 280, 720, 0xFF4755ff)
    start_btn = Button(win.mlx, win.mlx_ptr, win.win, 380, 141, 250, 50, 0xff272727, "Generate Maze", text_color=0xFFFFFFFF)
    bg_btn = Button(win.mlx, win.mlx_ptr, win.win, 304, 208, 150, 50, 0xff272727, "BG Color", text_color=0xFFFFFFFF)
    wall_btn = Button(win.mlx, win.mlx_ptr, win.win, 304, 357, 150, 50, 0xff272727, "Wall Color", text_color=0xFFFFFFFF)
    cell_btn = Button(win.mlx, win.mlx_ptr, win.win, 545, 208, 150, 50, 0xff272727, "Cell Color", text_color=0xFFFFFFFF)
    patt_btn = Button(win.mlx, win.mlx_ptr, win.win, 545, 357, 150, 50, 0xff272727, "42 Color", text_color=0xFFFFFFFF)
    
    # Color picker buttons for BG (3x2 grid, 30x30 each, 30px h-gap, 5px v-gap)
    bg_colors = [
        Button(win.mlx, win.mlx_ptr, win.win, 304, 264, 30, 30, 0xFFFFFFFF, "", on_click=set_bg_color(0xFFFFFFFF)),
        Button(win.mlx, win.mlx_ptr, win.win, 364, 264, 30, 30, 0xFFF0F0F0, "", on_click=set_bg_color(0xFFF0F0F0)),
        Button(win.mlx, win.mlx_ptr, win.win, 424, 264, 30, 30, 0xFF222222, "", on_click=set_bg_color(0xFF222222)),
        Button(win.mlx, win.mlx_ptr, win.win, 304, 299, 30, 30, 0xFFCAE9FF, "", on_click=set_bg_color(0xFFCAE9FF)),
        Button(win.mlx, win.mlx_ptr, win.win, 364, 299, 30, 30, 0xFFE1F3E6, "", on_click=set_bg_color(0xFFE1F3E6)),
        Button(win.mlx, win.mlx_ptr, win.win, 424, 299, 30, 30, 0xFFFFFACD, "", on_click=set_bg_color(0xFFFFFACD))
    ]
    
    # Color picker buttons for Cell
    cell_colors = [
        Button(win.mlx, win.mlx_ptr, win.win, 545, 264, 30, 30, 0xFF2196F3, "", on_click=set_cell_color(0xFF2196F3)),
        Button(win.mlx, win.mlx_ptr, win.win, 605, 264, 30, 30, 0xFFE53935, "", on_click=set_cell_color(0xFFE53935)),
        Button(win.mlx, win.mlx_ptr, win.win, 665, 264, 30, 30, 0xFFFB8C00, "", on_click=set_cell_color(0xFFFB8C00)),
        Button(win.mlx, win.mlx_ptr, win.win, 545, 299, 30, 30, 0xFF43A047, "", on_click=set_cell_color(0xFF43A047)),
        Button(win.mlx, win.mlx_ptr, win.win, 605, 299, 30, 30, 0xFF8E24AA, "", on_click=set_cell_color(0xFF8E24AA)),
        Button(win.mlx, win.mlx_ptr, win.win, 665, 299, 30, 30, 0xFF00BCD4, "", on_click=set_cell_color(0xFF00BCD4))
    ]
    
    # Color picker buttons for Wall
    wall_colors = [
        Button(win.mlx, win.mlx_ptr, win.win, 304, 413, 30, 30, 0xFF000000, "", on_click=set_wall_color(0xFF000000)),
        Button(win.mlx, win.mlx_ptr, win.win, 364, 413, 30, 30, 0xFFFFFFFF, "", on_click=set_wall_color(0xFFFFFFFF)),
        Button(win.mlx, win.mlx_ptr, win.win, 424, 413, 30, 30, 0xFF424242, "", on_click=set_wall_color(0xFF424242)),
        Button(win.mlx, win.mlx_ptr, win.win, 304, 448, 30, 30, 0xFFBDBDBD, "", on_click=set_wall_color(0xFFBDBDBD)),
        Button(win.mlx, win.mlx_ptr, win.win, 364, 448, 30, 30, 0xFF3F51B5, "", on_click=set_wall_color(0xFF3F51B5)),
        Button(win.mlx, win.mlx_ptr, win.win, 424, 448, 30, 30, 0xFF800000, "", on_click=set_wall_color(0xFF800000))
    ]
    
    # Color picker buttons for Pattern
    patt_colors = [
        Button(win.mlx, win.mlx_ptr, win.win, 545, 413, 30, 30, 0xFFFF4081, "", on_click=set_pattern_color(0xFFFF4081)),
        Button(win.mlx, win.mlx_ptr, win.win, 605, 413, 30, 30, 0xFFFFD700, "", on_click=set_pattern_color(0xFFFFD700)),
        Button(win.mlx, win.mlx_ptr, win.win, 665, 413, 30, 30, 0xFF00FF00, "", on_click=set_pattern_color(0xFF00FF00)),
        Button(win.mlx, win.mlx_ptr, win.win, 545, 448, 30, 30, 0xFF87CEEB, "", on_click=set_pattern_color(0xFF87CEEB)),
        Button(win.mlx, win.mlx_ptr, win.win, 605, 448, 30, 30, 0xFF673AB7, "", on_click=set_pattern_color(0xFF673AB7)),
        Button(win.mlx, win.mlx_ptr, win.win, 665, 448, 30, 30, 0xFFFF9800, "", on_click=set_pattern_color(0xFFFF9800))
    ]

    quit_btn = Button(win.mlx, win.mlx_ptr, win.win, 400, 530, 200, 50, 0xff272727, "Quit", text_color=0xFFFFFFFF)
    
    win.mlx.mlx_loop(win.mlx_ptr)


if __name__ == "__main__":
    main()


