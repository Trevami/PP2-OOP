import pygame
from classes.RectSubsurface import RectSubsurface


class Button(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "color": pygame.Color(85, 85, 85),
            "color_pressed": pygame.Color(155, 155, 155),
            "pressed": False,
        }
        kwargs = defaultKwargs | kwargs
        self.pressed = kwargs["pressed"]
        self.color = kwargs["color"]
        self.color_pressed = kwargs["color_pressed"]

    def update_toggle(self):
        if self.pressed:
            self.pressed = False
        else:
            self.pressed = True

    def _draw_unpressed(self):
        self.surf.fill(self.color)

    def _draw_pressed(self):
        self.surf.fill(self.color_pressed)
    
    def draw_update(self):
        if self.pressed:
            self._draw_pressed()
        else:
            self._draw_unpressed()