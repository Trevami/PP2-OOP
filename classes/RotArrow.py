import pygame
from functions.vectors_and_interpolation import get_vector


class RotArrow(pygame.sprite.Sprite):
    def __init__(self, constant, angle, line_width, arrow_head_size, circle=True):
        super(RotArrow, self).__init__()
        self.surf = pygame.Surface((abs(constant * 2), abs(constant * 2)))
        self.vector = get_vector(constant, angle)
        self.constant = constant # constant c_i
        self.time_factor = 1
        self.angle = angle
        self.anchor_x = 0
        self.anchor_y = 0
        self.color = pygame.Color(0, 0, 0)
        self.line_width = line_width
        self.head_rel_size = arrow_head_size
        self.draw_circle = circle
        self.update()

    def set_anchor(self, x, y):
        self.anchor_x = x
        self.anchor_y = y
        self.draw_update()

    def get_anchor(self):
        return (self.anchor_x, self.anchor_y)

    def rotate(self, degrees):
        self.vector = self.vector.rotate(-degrees)
        self.draw_update()

    def update(self):
        # Ticks in seconds * time_factor
        tick = pygame.time.get_ticks() / 1000 * self.time_factor
        self.vector = get_vector(self.constant, (tick * self.angle))
        self.draw_update()

    def clear_surface(self):
        self.surf.fill(pygame.Color(255, 255, 255))

    def _draw_arrow_line(self, center_pos: tuple):
        # Draw arrow line:
        pos_end_line = (center_pos[0] + self.vector.x, center_pos[1] + self.vector.y)
        pygame.draw.line(
            self.surf,
            self.color,
            center_pos,
            pos_end_line,
            width=self.line_width
        )

    def _draw_arrow_head(self, line_pos: tuple):
        # Draw arrow head:
        head_angle = 20  # Steepness of the arrow head
        vector_angle = self.vector.angle_to(pygame.math.Vector2(1, 0))
        # vt: vector top, vb: vector bottom, if arrow vector points to the right
        head_vt_angle = head_angle - vector_angle
        head_vt = pygame.math.Vector2(-self.head_rel_size,
                                      0).rotate(head_vt_angle)
        head_vb_angle = head_angle + vector_angle
        head_vb = pygame.math.Vector2(-self.head_rel_size,
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

    def _draw_arrow_circle(self, center_pos: tuple):
        # Draw arrow circle:
        if self.draw_circle:
            pygame.draw.circle(
                self.surf,
                self.color,
                center_pos,
                self.surf.get_width() / 2,
                self.line_width
            )

    def _draw_arrow(self):
        # Surface center pos.
        center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
        # End of arrow line pos. 
        pos_end_line = (center[0] + self.vector.x, center[1] + self.vector.y)

        self._draw_arrow_line(center)
        self._draw_arrow_head(pos_end_line)
        self._draw_arrow_circle(center)

    def draw_update(self):
        self.clear_surface()
        self._draw_arrow()
