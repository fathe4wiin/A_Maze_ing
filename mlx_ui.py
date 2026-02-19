from mlx import Mlx

class Window:
    def __init__(self, width, height, title, mlx_ptr=None, on_mouse=None, on_loop=None, on_key=None):
        self.mlx = Mlx()
        self.mlx_ptr = mlx_ptr if mlx_ptr else self.mlx.mlx_init()
        self.win = self.mlx.mlx_new_window(self.mlx_ptr, width, height, title)
        self.width = width
        self.height = height
        self.mlx.mlx_hook(self.win, 33, 0, self.close_window, None)
    
        if on_mouse:
            self.mlx.mlx_mouse_hook(self.win, on_mouse, None)
        if on_loop:
            self.mlx.mlx_loop_hook(self.mlx_ptr, on_loop, None)
        if on_key:
            self.mlx.mlx_key_hook(self.win, on_key, None)

    def close_window(self, param):
        self.mlx.mlx_loop_exit(self.mlx_ptr)
        return 0

    def draw_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

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
    
    def clear(self, color=0xFFFFFFFF):
        # Optimized clearing by drawing a big rect
        self.draw_filled_rect(0, 0, self.width, self.height, color)

    def destroy(self):
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win)


class Label:
    def __init__(self, mlx, mlx_ptr, win, x, y, text, color):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win = win
        self.x = x
        self.y = y
        self.text = text
        self.color = color

    def draw(self):
        """Draw the label on the window."""
        self.mlx.mlx_string_put(self.mlx_ptr, self.win, self.x, self.y, self.color, self.text)

class Button:
    def __init__(self, mlx, mlx_ptr, win, x, y, w, h, color, text, text_color=0xFFFFFFFF):
        self.mlx = mlx
        self.mlx_ptr = mlx_ptr
        self.win = win
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.text_color = text_color
        self.destroyed = False
        # Create a Label for the button text
        self.label = Label(mlx, mlx_ptr, win, x + 10, y + (h // 2) - 10, text, text_color)

    def draw(self):
        """Draw the button (rect + label) on the window."""
        if self.destroyed:
            return
        # Draw button background
        for i in range(self.x, self.x + self.w):
            for j in range(self.y, self.y + self.h):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, i, j, self.color)
        
        # Draw button label
        self.label.draw()

    def is_clicked(self, mx, my):
        """Check if mouse coordinates are inside the button."""
        if self.destroyed:
            return False
        return self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h

    def destroy(self):
        """Mark the button as destroyed so it won't be drawn."""
        self.destroyed = True

