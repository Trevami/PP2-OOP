import pygame
import numpy as np
import os
from classes.RectSubsurface import RectSubsurface


class Slider(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "min": 1.0,
            "max": 100.0,
            "ticks": 1,
            "start": None,
            "text": "Slider",
            "font_type": "",
            "font_size": 24,
            "font_margin": 3,
            "font_side_margin": 10,
            "bar_width": 10,
            "bar_color": pygame.Color(85, 85, 85),
            "bar_color_pressed": pygame.Color(155, 155, 155),
            "background_color": pygame.Color(15, 15, 15),
            "type": "int"
        }
        kwargs = defaultKwargs | kwargs
        self.bar_x_pos = 0
        self.bar_y_pos = 0
        self.value = kwargs["start"]
        self.value_text = kwargs["text"]
        self.font_type = kwargs["font_type"]
        self.font_size = kwargs["font_size"]
        self.font_margin = kwargs["font_margin"]
        self.font_side_margin = kwargs["font_side_margin"]
        self.bar_width = kwargs["bar_width"]
        self.bar_color = kwargs["bar_color"]
        self.bar_color_pressed = kwargs["bar_color_pressed"]
        self.background_color = kwargs["background_color"]
        self.type = kwargs["type"]
        self.pressed = False
        self.pos_value_lookup = self._get_value_pos_lookup(
            kwargs["min"], kwargs["max"], kwargs["ticks"])
        self._init_slider_bar_pos()

    def set_new_values(self, min_value: float, max_value: float, num_value_ticks: int):
        self.pos_value_lookup = self._get_value_pos_lookup(
            self, min_value, max_value, num_value_ticks)

    def set_draw_palette(self, palette: dict):
        self.bar_color = palette["bar_color"]
        self.bar_color_pressed = palette["bar_color_pressed"]
        self.background_color = palette["background_color"]

    def get_font(self):
        if self.font_type != "":
            return pygame.font.SysFont(self.font_type, self.font_size)
        else:
            font_name = "FantasqueSansMono-Regular.ttf"
            font_folder_name = "FantasqueSansMono"
            font_path = os.path.join(
                os.path.abspath(os.getcwd()),
                "resources",
                "fonts",
                font_folder_name,
                font_name
            )
            return pygame.font.Font(font_path, self.font_size)

    def get_font_size(self, value: float):
        # Returns the dimensions of the button text.
        return self.get_font().size(f"{self.value_text}: {value}")

    def get_font_height(self):
        # Returns the height of the slider text.
        return self.get_font().get_height()

    def _get_value_pos_lookup(self, min_value: float, max_value: float, num_value_ticks: int):
        self._input_check(min_value, max_value, num_value_ticks)

        # Gets the max width of the font:
        # Differences in type font width due to decimal places of float
        if self.type == "int":
            font_width = self.get_font_size(int(max_value))[0]
        else:
            font_width = self.get_font_size(float(max_value))[0]

        # Generates a lookup data table with x_pos and corresponding value data.
        x_min = self.bar_x_pos + font_width + self.font_side_margin
        x_max = self.surf.get_width() - self.bar_width

        # Generates a list with value data.
        value_delta = max_value - min_value
        rel_value_delta = value_delta / num_value_ticks
        values = [*np.arange(min_value, max_value, rel_value_delta)]
        values.append(float(max_value))

        # Generates a list of corresponding x_pos data.
        # Linear ratio calculation are used for x_pos calculation.
        x_pos_value_ratio = (x_max - x_min) / value_delta
        value_ticks_x_pos = [(value - min_value) *
                             x_pos_value_ratio + x_min for value in values]

        # Generates the output lookup table with tick x_pos : tick value entries.
        if self.type == "int":
            return {x_pos: int(value) for x_pos, value in zip(value_ticks_x_pos, values)}
        else:
            return {x_pos: float(value) for x_pos, value in zip(value_ticks_x_pos, values)}

    def _init_slider_bar_pos(self):
        # Sets the start position to the bar to specified position.
        # Linear ratio calculations are used for x_pos determination.
        # Value position will be lost after the x_pos of the bar is changed.
        # Minimum value is used if not specified in **kwargs.

        values = list(self.pos_value_lookup.values())
        x_pos = list(self.pos_value_lookup.keys())
        x_pos_value_ratio = (x_pos[-1] - x_pos[0]) / (values[-1] - values[0])

        if self.value and self.value >= values[0] and self.value <= values[-1]:
            if self.type == "int":
                # Converts to int for consistency.
                self.value = int(self.value)
            else:
                # Converts to float for consistency.
                self.value = float(self.value)

            # Sets position.
            self.bar_x_pos = (
                self.value - values[0]) * x_pos_value_ratio + x_pos[0]
        else:
            self.value = values[0]

    def _input_check(self, min_value: float, max_value: float, num_value_ticks: int):
        # Throws exceptions if wrong input for _get_value_pos_lookup().
        if min_value >= max_value:
            raise ValueError(
                f"Wrong range arguments min: {min_value}, max: {max_value}")
        if num_value_ticks < 0:
            raise ValueError(
                f"Invalid ticks argument of {num_value_ticks}, must be > 0")
        if self.type != "int" and self.type != "float":
            raise ValueError(
                f"Invalid type argument {self.type}, must be int or float")

    def _adjust_text_size(self):
        for size in range(self.font_size, 1, -1):
            font_height = self.get_font_height()
            surf_dim = self.surf.get_size()

            if not font_height <= (surf_dim[1] - 2 * self.font_margin):
                self.font_size = size
            else:
                break

    def update_x_pos(self, x_pos: float):
        # Sets the input x_pos to the center of the bar.
        x_pos = x_pos - self.bar_width / 2 - self.surf.get_abs_offset()[0]

        # Gets a list of all possible x_pos values.
        value_pos = list(self.pos_value_lookup.keys())

        # Iterates trough possible x_pos pairs and checks if input x_pos is near to one.
        # Sets the new x_pos of the bar to a set x_pos if input x_pos is near to it.
        for i in range(1, len(value_pos)):
            if x_pos >= value_pos[i - 1] and x_pos <= value_pos[i]:
                if abs(x_pos - value_pos[i]) < abs(x_pos - value_pos[i - 1]):
                    self.bar_x_pos = value_pos[i]
                    self.value = self.pos_value_lookup[value_pos[i]]
                else:
                    self.bar_x_pos = value_pos[i - 1]
                    self.value = self.pos_value_lookup[value_pos[i - 1]]

    def _draw_bar(self):
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

    def _draw_text(self):
        # Draw text:
        text = self.get_font().render(
            f"{self.value_text}: {self.value}", True, self.bar_color_pressed)
        # Draw text:
        self.surf.blit(text, (self.font_side_margin, self.font_margin))

    def draw_update(self):
        # Fills background with color.
        self.surf.fill(self.background_color)
        self._adjust_text_size()

        self._draw_bar()
        self._draw_text()
