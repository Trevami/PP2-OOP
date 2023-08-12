import pygame
from classes.RectSubsurface import RectSubsurface


class TraceSubsurface(RectSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height)
        defaultKwargs = {
            "surf_color": pygame.Color(0, 0, 0),
            "trace_color": pygame.Color(100, 220, 0),
            "trace_width": 2,
            "cross_color": pygame.Color(25, 22, 20),
            "cross_size": 6,
            "cross_line_width": 3,
            "cross": True
        }
        kwargs = defaultKwargs | kwargs
        self.trace = []
        self.surf_color = kwargs["surf_color"]
        self.trace_color = kwargs["trace_color"]
        self.trace_width = kwargs["trace_width"]
        self.cross_color = kwargs["cross_color"]
        self.cross_size = kwargs["cross_size"]
        self.cross_line_width = kwargs["cross_line_width"]
        self.cross = kwargs["cross"]

    def append_trace_pt(self, point):
        self.trace.append(point)

    def clear_trace(self):
        self.trace.clear()

    def draw_trace(self):
        if len(self.trace) >= 2:
            pygame.draw.lines(
                self.surf,
                self.trace_color,
                False,
                self.trace,
                width=self.trace_width
            )

    def set_draw_palette(self, palette: dict):
        self.surf_color = palette["surf_color"]
        self.trace_color = palette["trace_color"]
        self.cross_color = palette["cross_color"]

    def draw_cross(self):
        if self.cross:
            center = (self.surf.get_width() / 2, self.surf.get_height() / 2)
            cross_points = [
                ((center[0] - self.cross_size,  center[1] - self.cross_size),
                 (center[0] + self.cross_size,  center[1] + self.cross_size)),
                ((center[0] + self.cross_size,  center[1] - self.cross_size),
                 (center[0] - self.cross_size,  center[1] + self.cross_size))
            ]

            for pt1, pt2 in cross_points:
                pygame.draw.line(
                    self.surf,
                    self.cross_color,
                    pt1,
                    pt2,
                    self.cross_line_width
                )