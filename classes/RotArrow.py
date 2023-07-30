import pygame
from functions.vectors_and_interpolation import get_vector


class RotArrow(pygame.sprite.Sprite):
    def __init__(self, constant: float, angle: float, **kwargs):
        super(RotArrow, self).__init__()
        defaultKwargs = {
            "time_factor": 1,
            "anchor_x": 0,
            "anchor_y": 0,
            "color": pygame.Color(80, 80, 80),
            "circle_color": pygame.Color(80, 80, 80),
            "line_width": 1,
            "head_size": 10,
            "circle": True
        }
        kwargs = defaultKwargs | kwargs
        self.surf = pygame.Surface((abs(constant * 2), abs(constant * 2)))
        self.vector = get_vector(constant, angle)
        self.constant = constant  # constant c_i
        self.angle = angle
        self.time_factor = kwargs["time_factor"]
        self.anchor_x = kwargs["anchor_x"]
        self.anchor_y = kwargs["anchor_y"]
        self.color = kwargs["color"]
        self.circle_color = kwargs["circle_color"]
        self.line_width = kwargs["line_width"]
        self.head_size = kwargs["head_size"]
        self.circle = kwargs["circle"]
        self.update()

    def set_anchor(self, pos: tuple):
        """Sets the center blit position (anchor position) of the RotArrow Sprite.

        Args:
            pos (tuple): new anchor position (x, y)
        """
        self.anchor_x = pos[0]
        self.anchor_y = pos[1]

    def get_anchor(self):
        """Returns the center blit position (anchor position) of the RotArrow Sprite.

        Returns:
            tuple: anchor position (x, y)
        """
        return (self.anchor_x, self.anchor_y)

    def rotate(self, degrees: float):
        """Rotates the RotArrow Sprite in the clockwise direction.

        Args:
            degrees (float): degrees of rotation
        """
        self.vector = self.vector.rotate(-degrees)

    def update(self):
        """Updates the rotation of the RotArrow Sprite.
        """
        # Ticks in seconds * time_factor
        tick = pygame.time.get_ticks() / 1000 * self.time_factor
        self.vector = get_vector(self.constant, (tick * self.angle))

    def clear_surface(self):
        """Removes all pixels from the draw surface. 
        """
        self.surf.fill(pygame.Color(255, 255, 255))
        self.surf.set_colorkey(pygame.Color(255, 255, 255))

    def _update_head_size(self):
        """Updates the head size of the arrow to half the arrow size if the arrow is smaller than half the specified head size.
        """
        if self.surf.get_width() < (self.head_size * 2):
            self.head_size = self.surf.get_width() / 2

    def _draw_arrow_line(self, pos: tuple):
        """Draws the arrow line onto the draw surface.

        Args:
            pos (tuple): first point position (x, y)
        """
        pos_end_line = (pos[0] + self.vector.x, pos[1] + self.vector.y)
        pygame.draw.line(
            self.surf,
            self.color,
            pos,
            pos_end_line,
            width=self.line_width
        )

    def _draw_arrow_head(self, line_pos: tuple):
        """Draws the arrow head at the end of the arrow line onto the draw surface.

        Args:
            line_pos (tuple): last point position (x, y) of the arrow line.
        """
        # Draw arrow head:
        head_angle = 20  # Steepness of the arrow head
        vector_angle = self.vector.angle_to(pygame.math.Vector2(1, 0))
        # vt: vector top, vb: vector bottom, if arrow vector points to the right
        head_vt_angle = head_angle - vector_angle
        head_vt = pygame.math.Vector2(-self.head_size,
                                      0).rotate(head_vt_angle)
        head_vb_angle = head_angle + vector_angle
        head_vb = pygame.math.Vector2(-self.head_size,
                                      0).rotate(-head_vb_angle)
        pos_head = [
            (line_pos[0] + head_vt.x, line_pos[1] + head_vt.y),
            line_pos,
            (line_pos[0] + head_vb.x, line_pos[1] + head_vb.y)
        ]
        pygame.draw.polygon(
            self.surf,
            self.color,
            pos_head
        )

    def _draw_arrow_circle(self, pos: tuple):
        """Draws a circle at the specified position onto the draw surface.

        Args:
            pos (tuple): center position (x, y) of the circle.
        """
        if self.circle:
            pygame.draw.circle(
                self.surf,
                self.circle_color,
                pos,
                self.surf.get_width() / 2,
                self.line_width
            )

    def _draw_arrow(self):
        """Draws the arrow onto the draw circle.
        """
        # Surface center pos.
        center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
        # End of arrow line pos.
        pos_end_line = (center[0] + self.vector.x, center[1] + self.vector.y)

        self._draw_arrow_line(center)
        self._draw_arrow_head(pos_end_line)
        self._draw_arrow_circle(center)

    def draw_update(self):
        """Draw update for the arrow draw surface.
        Clears the draw surface and redraws the arrow. 
        """
        self.clear_surface()
        self._update_head_size()
        self._draw_arrow()
