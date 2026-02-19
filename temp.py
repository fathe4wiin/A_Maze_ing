from mlx import Mlx

class Label:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color

    def draw(self, mlx, mlx_ptr, win):
        """Draw the label on the window."""
        # Using mlx_string_put with encoded string as required by Python bindings often
        mlx.mlx_string_put(mlx_ptr, win, self.x, self.y, self.color, self.text)

class Button:
    def __init__(self, x, y, w, h, color, text, text_color=0xFFFFFFFF):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.text = text
        self.text_color = text_color
        # Create a Label for the button text, centered roughly
        # Centering text perfectly requires knowing text width, which mlx usually doesn't provide easily.
        # We'll use a simple offset.
        self.label = Label(x + 10, y + (h // 2) - 10, text, text_color)

    def draw(self, mlx, mlx_ptr, win):
        """Draw the button (rect + label) on the window."""
        # Draw button background
        for i in range(self.x, self.x + self.w):
            for j in range(self.y, self.y + self.h):
                mlx.mlx_pixel_put(mlx_ptr, win, i, j, self.color)
        
        # Draw button label
        self.label.draw(mlx, mlx_ptr, win)

    def is_clicked(self, mx, my):
        """Check if mouse coordinates are inside the button."""
        return self.x <= mx <= self.x + self.w and self.y <= my <= self.y + self.h


# --- Usage Example ---
if __name__ == "__main__":
    mlx = Mlx()
    mlx_ptr = mlx.mlx_init()
    win = mlx.mlx_new_window(mlx_ptr, 800, 600, "Button and Label Demo")

    # Create instances
    lbl = Label(350, 50, "My Game Menu", 0xFFFFFF00)
    btn = Button(300, 200, 200, 50, 0xFF0000FF, "Click Me!", 0xFFFFFFFF)

    for x in range(800):
        for y in range(600):
            mlx.mlx_pixel_put(mlx_ptr, win, x, y, 0xFF000000)
    def render_loop(_):
        # In a real loop, you might clear the screen first.
        # Here we just redraw the UI elements.
        lbl.draw(mlx, mlx_ptr, win)
        btn.draw(mlx, mlx_ptr, win)

    def mouse_hook(button, x, y, _):
        if btn.is_clicked(x, y):
            print("Button was clicked!")
            # Change color on click as feedback
            btn.color = 0xFF00FF00 

    mlx.mlx_mouse_hook(win, mouse_hook, None)
    mlx.mlx_loop_hook(mlx_ptr, render_loop, None)
    mlx.mlx_loop(mlx_ptr)
