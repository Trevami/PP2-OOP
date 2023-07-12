import pygame
import numpy as np


class Slider(pygame.Rect):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(left, top, width, height)
        defaultKwargs = {
            "min": 1.0,
            "max": 100.0,
            "ticks": 1,
            "start": None,
            "text": "Slider",
            "font": pygame.font.SysFont("Arial", 24),
            "font_margin": 10,
            "bar_width": 10,
            "bar_color": pygame.Color(85, 85, 85),
            "bar_color_pressed": pygame.Color(155, 155, 155),
            "background_color": pygame.Color(15, 15, 15),
            "type": "int"
            }
        kwargs = defaultKwargs | kwargs
        self.surf = surf.subsurface(self)
        self.bar_x_pos = 0
        self.bar_y_pos = 0
        self.value = kwargs["start"]
        self.value_text = kwargs["text"]
        self.font = kwargs["font"]
        self.font_margin = kwargs["font_margin"]
        self.bar_width = kwargs["bar_width"]
        self.bar_color = kwargs["bar_color"]
        self.bar_color_pressed = kwargs["bar_color_pressed"]
        self.background_color = kwargs["background_color"]
        self.type = kwargs["type"]
        self.pressed = False
        self.value_pos_lookup = self._get_value_pos_lookup(kwargs["min"], kwargs["max"], kwargs["ticks"])

    def get_font_width(self, value: float):
        font = self.font.render(f"{self.value_text}: {value}", True, pygame.Color(0, 0, 0))
        return font.get_width()

    def _get_value_pos_lookup(self, min_value: float, max_value: float, num_value_ticks: int):
        # Throws exceptions if wrong input.
        if min_value >= max_value:
            raise ValueError(f"Wrong range arguments min: {min_value}, max: {max_value}")
        if num_value_ticks < 0:
            raise ValueError(f"Invalid ticks argument of {num_value_ticks}, must be > 0")
        if self.type != "int" and self.type != "float":
            raise ValueError(f"Invalid type argument {self.type}, must be int or float")
        
        # Gets the width of the font:
        # Differences in type font width due to decimal places of float
        if self.type == "int":
            font_width = self.get_font_width(int(max_value))
        else:
            font_width = self.get_font_width(float(max_value))
        
        # Generates a lookup data table with x_pos and corresponding value data.
        x_min = self.bar_x_pos + font_width + self.font_margin
        x_max = self.surf.get_width() - self.bar_width
        # Generates a list with value data.
        value_delta = max_value - min_value
        rel_value_delta = value_delta / num_value_ticks
        values = [*np.arange(min_value, max_value, rel_value_delta)]
        values.append(float(max_value))
        # Generates a list of corresponding x_pos data.
        # Linear ratio calculation are used for x_pos calculation.
        x_pos_value_ratio = (x_max - x_min) / value_delta
        value_ticks_x_pos = [(value - values[0]) * x_pos_value_ratio + x_min for value in values]
        # Fills the output lookup table with tick x_pos : tick value entries.
        value_lookup = {}
        for i in range(len(values)):
            if self.type == "int":
                value_lookup.update({value_ticks_x_pos[i]: int(values[i])})
            else:
                value_lookup.update({value_ticks_x_pos[i]: float(values[i])})

        # Sets the start position to the bar to specified position.
        # Linear ratio calculations are used for x_pos determination.
        # Value position will be lost after the x_pos of the bar is changed.
        # Minimum value is used if not specified in **kwargs.
        if self.value and self.value >= values[0] and self.value <= values[-1]:
            if self.type == "int":
                self.value = int(self.value) # Converts to int for consistency.
            else:
                self.value = float(self.value) # Converts to float for consistency.
            
            # Sets position.
            self.bar_x_pos = (self.value - values[0]) * x_pos_value_ratio + x_min
        else:
            self.value = min_value

        return value_lookup
    
    def set_new_values(self, min_value: float, max_value: float, num_value_ticks: int):
        self.value_pos_lookup = self._get_value_pos_lookup(self, min_value, max_value, num_value_ticks)
    
    def draw_slider(self):
        # Fills background with color.
        self.surf.fill(self.background_color)

        # Draw bar:
        rect_width = self.bar_width
        rect_height = self.surf.get_height()
        slider_bar = pygame.Rect(
            self.bar_x_pos,
            self.bar_y_pos,
            rect_width,
            rect_height
        )
        # Will change color if self.pressed is set to True.
        if self.pressed:
            bar_color = self.bar_color_pressed
        else:
            bar_color = self.bar_color
        pygame.draw.rect(
            self.surf,
            bar_color,
            slider_bar
        )

        # Draw arrow text:
        arrow_text = self.font.render(f"{self.value_text}: {self.value}", True, self.bar_color_pressed)
        # Draw text:
        self.surf.blit(arrow_text, (self.font_margin, 0))

    def update_x_pos(self, x_pos: float):
        # Sets the input x_pos to the center of the bar.
        x_pos = x_pos - self.bar_width / 2 - self.surf.get_abs_offset()[0]

        # Gets a list of all possible x_pos values.
        value_pos = list(self.value_pos_lookup.keys())

        # Iterates trough possible x_pos pairs and checks if input x_pos is near to one.
        # Sets the new x_pos of the bar to a set x_pos if input x_pos is near to it.
        for i in range(1, len(value_pos)):
            if x_pos >= value_pos[i - 1] and x_pos <= value_pos[i]:
                if abs(x_pos - value_pos[i]) < abs(x_pos - value_pos[i - 1]):
                    self.bar_x_pos = value_pos[i]
                    self.value = self.value_pos_lookup[value_pos[i]]
                else:
                    self.bar_x_pos = value_pos[i - 1]
                    self.value = self.value_pos_lookup[value_pos[i - 1]]

    def set_draw_palette(self, palette: dict):
        self.bar_color = palette["bar_color"]
        self.bar_color_pressed = palette["bar_color_pressed"]
        self.background_color = palette["background_color"]