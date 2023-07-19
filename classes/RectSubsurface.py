import pygame


class RectSubsurface(pygame.Rect):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float):
        super().__init__(left, top, width, height)
        self.surf = surf.subsurface(self)

    def get_abs_bbox(self):
        """Returns the bounding box with the absolute position inside its top level parent.

        Returns:
            pygame.Rect: abs bounding box of subsurface
        """
        rect = self.surf.get_rect()
        abs_pos = self.surf.get_abs_offset()
        rect.left = abs_pos[0]
        rect.top = abs_pos[1]
        return rect
