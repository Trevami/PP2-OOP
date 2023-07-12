import pygame
from functions.vectors_and_interpolation import get_shape_length, lin_interpolate
from classes.TraceSurface import TraceSurface


class DrawSurface(TraceSurface):
    def __init__(self, size: tuple, *args, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.surf_color = pygame.Color(50, 50, 50)

    def close_trace(self):
        # Linear interpolation between last and first point of trace.
        if len(self.trace) >= 3:
            # Gets first and last point of shape line.
            pt1 = self.trace[0]
            pt2 = self.trace[-1]

            # Calculates the number of interpol points from the average point distance.
            av_point_dist = get_shape_length(self.trace) / len(self.trace)
            dist = pygame.math.Vector2(pt2[0] - pt1[0], pt2[1] - pt1[1]).length()
            num_points = int(round(dist / av_point_dist, 0))

            # Linear interpolation:
            self.trace.extend(lin_interpolate(pt2, pt1, num_points))
            self.trace.append(pt1) # Closes gap between points.