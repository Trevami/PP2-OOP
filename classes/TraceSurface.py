import pygame


class TraceSurface(pygame.Surface):
    def __init__(self, size, *args, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.trace = []
        self.surf_color = pygame.Color(0, 0, 0)
        self.trace_color = pygame.Color(100, 220, 0)
        self.trace_width = 2
        self.cross_color = pygame.Color(25, 22, 20)
        self.cross_size = 6
        self.cross_line_width = 3
        self.cross = True

    def append_trace_pt(self, point):
        self.trace.append(point)

    def clear_trace(self):
        self.trace.clear()

    def draw_trace(self):
        pygame.draw.lines(
            self,
            self.trace_color,
            False,
            self.trace,
            width=self.trace_width
        )

    def set_draw_palette(self, palette: dict):
        self.surf_color = palette["surf_color"]
        self.trace_color = palette["trace_color"]
        self.cross_color = palette["cross_color"]

    def clear_surface(self):
        self.fill(self.surf_color)

    def draw_cross(self):
        if self.cross:
            center = (self.get_width() / 2, self.get_height() / 2)
            cross_points = [
                ((center[0] - self.cross_size,  center[1] - self.cross_size),
                 (center[0] + self.cross_size,  center[1] + self.cross_size)),
                ((center[0] + self.cross_size,  center[1] - self.cross_size),
                 (center[0] - self.cross_size,  center[1] + self.cross_size))
            ]

            for pt1, pt2 in cross_points:
                pygame.draw.line(
                    self,
                    self.cross_color,
                    pt1,
                    pt2,
                    self.cross_line_width
                )

    def draw_update(self):
        self.clear_surface()
        self.draw_cross()
        if len(self.trace) >= 2:
            self.draw_trace()
