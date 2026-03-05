from mlx import Mlx

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
    def clear(self, bg):
        self.draw_filled_rect(self.x, self.y, len(self.text) * 10, 20, bg)

    def update(self, bg, text=None):
        self.clear(bg)
        if text is not None:
            self.text = text
        self.draw()

    def draw_filled_rect(self, x, y, width, height, color):
        for i in range(x, x + width):
            for j in range(y, y + height):
                self.draw_pixel(i, j, color)

    def draw_pixel(self, x, y, color):
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, x, y, color)

class Button:
    def __init__(self, mlx, mlx_ptr, win, x, y, w, h, color, text, text_color=0xFFFFFFFF, on_click=None):
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
        self.on_click = on_click

        self.label = Label(mlx, mlx_ptr, win, x + 10, y + (h // 2) - 10, text, text_color)

    def draw(self):
        """Draw the button (rect + label) on the window."""
        if self.destroyed:
            return

        for i in range(self.x, self.x + self.w):
            for j in range(self.y, self.y + self.h):
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win, i, j, self.color)

        self.label.draw()

    def is_clicked(self, mx, my):
        """Check if mouse coordinates are inside the button."""
        if self.destroyed:
            return False
        return self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h

    def handle_click(self, mx, my):
        """Check if clicked and execute callback if set."""
        if self.is_clicked(mx, my) and self.on_click:
            self.on_click()
            return True
        return False

    def destroy(self):
        """Mark the button as destroyed so it won't be drawn."""
        self.destroyed = True


