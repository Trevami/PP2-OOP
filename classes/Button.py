import pygame
import os
from classes.RectSubsurface import RectSubsurface


class Button(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "pressed": False,
            "color": pygame.Color(85, 85, 85),
            "color_pressed": pygame.Color(155, 155, 155),
            "text": "",
            "font_type": "",
            "font_size": 24,
            "font_margin": 10
        }
        kwargs = defaultKwargs | kwargs
        self.pressed = kwargs["pressed"]
        self.color = kwargs["color"]
        self.color_pressed = kwargs["color_pressed"]
        self.text = kwargs["text"]
        self.font_type = kwargs["font_type"]
        self.font_size = kwargs["font_size"]
        self.font_margin = kwargs["font_margin"]

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

    def get_font_size(self):
        # Returns the dimensions of the button text.
        return self.get_font().size(self.text)
    
    def _adjust_text_size(self):
        for size in range(self.font_size, 1, -1):
            font_size = self.get_font_size()
            surf_dim = self.surf.get_size()

            width_match = font_size[0] <= (surf_dim[0] - 2 * self.font_margin)
            height_match = font_size[1] <= (surf_dim[1] - 2 * self.font_margin) 

            if not width_match and not height_match:
                self.font_size = size
            else:
                break

    def update_toggle(self):
        if self.pressed:
            self.pressed = False
        else:
            self.pressed = True

    def _draw_unpressed(self):
        self.surf.fill(self.color)

    def _draw_pressed(self):
        self.surf.fill(self.color_pressed)

    def _draw_text(self, color):
        if self.text != "":
            button_center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
            text_center = (self.get_font_size()[0] / 2, self.get_font_size()[1] / 2)
            delta_centers = (button_center[0] - text_center[0], button_center[1] - text_center[1])
            # Draw text:
            text = self.get_font().render(f"{self.text}", True, color)
            self.surf.blit(text, (delta_centers[0], delta_centers[1]))
    
    def draw_update(self):
        self._adjust_text_size()
        if self.pressed:
            self._draw_pressed()
            self._draw_text(self.color)
        else:
            self._draw_unpressed()
            self._draw_text(self.color_pressed)