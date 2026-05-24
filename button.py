from pyray import *


class Button:
    def __init__(self, x, y, width, height, label, font, font_size, color=LIGHTGRAY, text_color=BLACK):
        self.bounds = Rectangle(x, y, width, height)
        self.label = label
        self.font = font
        self.font_size = font_size
        self.color = color
        self.text_color = text_color
        self.spacing = 1
        self.roundness = 0.5
        self.border_thickness = 10

    def contains(self, point=None):
        if point is None:
            point = get_mouse_position()
        return check_collision_point_rec(point, self.bounds)

    def draw(self):
        draw_rectangle_rounded(self.bounds, self.roundness, self.border_thickness, self.color)
        text_size = measure_text_ex(self.font, self.label, self.font_size, self.spacing)
        text_position = Vector2(
            self.bounds.x + (self.bounds.width - text_size.x) / 2,
            self.bounds.y + (self.bounds.height - text_size.y) / 2,
        )
        draw_text_ex(self.font, self.label, text_position, self.font_size, self.spacing, self.text_color)
