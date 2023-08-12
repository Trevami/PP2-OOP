import pygame
from classes.TraceSubsurface import TraceSubsurface
from classes.SettingsOverlay import SettingsOverlay
from functions.vectors_and_interpolation import get_shape_length, lin_interpolate
from functions.setting_elements.DrawSetElements import create_draw_setting_objs


class DrawSubsurface(TraceSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height, **kwargs)
        defaultKwargs = {
            "surf_color": pygame.Color(50, 50, 50),
            "show_shape_points": False,
            "shape_point_color": pygame.Color(200, 80, 0)
        }
        kwargs = defaultKwargs | kwargs
        self.surf_color = kwargs["surf_color"]
        self.shape_point_color = kwargs["shape_point_color"]
        self.settigs_overlay = self._create_settings_overlay()
        self.show_shape_points = kwargs["show_shape_points"]

    def close_trace(self):
        # Linear interpolation between last and first point of trace.
        if len(self.trace) >= 3:
            # Gets first and last point of shape line.
            pt1 = self.trace[0]
            pt2 = self.trace[-1]

            # No interpolation if shape is closed.
            if round(pt1[0], 2) == round(pt2[0], 2) and round(pt1[1], 2) == round(pt2[1], 2):
                return

            # Calculates the number of interpol points from the average point distance.
            av_point_dist = get_shape_length(self.trace) / len(self.trace)
            dist = pygame.math.Vector2(pt2[0] - pt1[0], pt2[1] - pt1[1]).length()
            num_points = int(round(dist / av_point_dist, 0))

            # Linear interpolation:
            self.trace.extend(lin_interpolate(pt2, pt1, num_points))
            self.trace.append(pt1) # Closes gap between points.

    def _create_settings_overlay(self):
        settings_overlay = SettingsOverlay(
            self,
            0,
            0,
            self.surf.get_width(),
            self.surf.get_height(),
            show=False,
        )
        create_draw_setting_objs(settings_overlay)
        return settings_overlay
    
    def _draw_settigs_overlay(self):
        self.settigs_overlay.draw_update()

    def _draw_shape_points(self):
        if self.show_shape_points and len(self.trace) >= 3:
            for point in self.trace:
                pygame.draw.circle(
                    self.surf,
                    self.shape_point_color,
                    point,
                    3
                )

    def draw_update(self):
        self.surf.fill(self.surf_color)
        self.draw_cross()
        self.draw_trace()
        self._draw_shape_points()
        self._draw_settigs_overlay()
