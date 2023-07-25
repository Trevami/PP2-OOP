import pygame
import math
import cmath
import numpy as np


def get_vector(lenght: float, angle: float):
    """Returns a PyGame Vector2 with the given length and angle.

    Args:
        lenght (float): vector length
        angle (float): vector angle

    Returns:
        pygame.math.Vector2: vector with input parameters
    """
    z = lenght * cmath.exp(angle * 2 * math.pi * -1j)
    return pygame.math.Vector2(z.real, z.imag)


def get_vec_screen_pos(arrow):
    """Calculates the absolute (x, y) position of the arrow on the blited surface.

    Args:
        arrow (Arrow): Arrow vector object

    Returns:
        tuple: (x, y) position of arrow vector
    """
    vec_screen_pos = (
        arrow.anchor_x + arrow.surf.get_width() / 2 + arrow.vector.x,
        arrow.anchor_y + arrow.surf.get_height() / 2 + + arrow.vector.y
    )
    return vec_screen_pos


def get_dist_points(point1: tuple, point2: tuple):
    """Calculates the distance between two (x, y) points.

    Args:
        point1 (tuple): first point (x, y)
        point2 (tuple): second point (x, y)

    Returns:
        float: distance between point1 and point2
    """
    dist_x = abs(point2[0] - point1[0])
    dist_y = abs(point2[1] - point1[1])
    return math.sqrt(dist_x**2 + dist_y**2)


def scale_vector(vector: pygame.math.Vector2, new_length: float):
    """Rescales a PyGame Vector2. New pygame.math.Vector2 will be returned.

    Args:
        vector (pygame.math.Vector2): vector to rescale
        new_length (float): length of new vector

    Returns:
        pygame.math.Vector2: new rescaled vector
    """
    norm_vect = vector.normalize()
    new_vect_x = norm_vect[0] * new_length
    new_vect_y = norm_vect[1] * new_length
    return pygame.math.Vector2(new_vect_x,  new_vect_y)


def lin_interpolate(point1: tuple, point2: tuple, num_interpol_pts: int):
    """Linear equidistant x, y interpolation between two points.
    Number of points can be specified.
    Only interpolated points are returned.

    Args:
        point1 (tuple): first interpolation point (x, y)
        point2 (tuple): last interpolation point (x, y)
        num_interpol_pts (int): number of interpolated points

    Returns:
        list: list of interpolated point tuples (x, y)
    """
    if num_interpol_pts < 1:
        return []
    # Calculates interpolated x and y values.
    dist_vect = pygame.math.Vector2(
        point2[0] - point1[0], point2[1] - point1[1])
    incr_vect = scale_vector(
        dist_vect, dist_vect.length() / (num_interpol_pts + 1))

    # Circumvents a division by 0 error if x or y position of both points are the same.
    # If axis coordinates are the same, generates a list with the axis coordinate.
    if point1[0] == point2[0]:
        y_new = list(np.arange(point1[1], point2[1], incr_vect[1]))
        x_new = [point1[0] for _ in range(len(y_new))]
    elif point1[1] == point2[1]:
        x_new = list(np.arange(point1[0], point2[0], incr_vect[0]))
        y_new = [point1[1] for _ in range(len(x_new))]
    else:
        x_new = list(np.arange(point1[0], point2[0], incr_vect[0]))
        y_new = list(np.arange(point1[1], point2[1], incr_vect[1]))

    # Removes additional x or y values if present.
    if len(x_new) > len(y_new):
        x_new.pop(-1)
    elif len(x_new) < len(y_new):
        y_new.pop(-1)

    # Only interpolated points are returned.
    return [(x_new[i], y_new[i]) for i in range(1, len(x_new))]


def get_shape_length(shape: list):
    """Calculates the distance between all given shape points.

    Args:
        shape (list): list of shape point tuples (x, y)

    Returns:
        float/int: length of shape
    """
    shape_length = 0
    for i in range(1, len(shape)):
        shape_length += get_dist_points(
            shape[i - 1], shape[i])
    return shape_length


def lin_interpolate_shape(shape: list, num_new_pts: int):
    """Linear interpolation for shape points. Duplicate points will be removed (reduced shape).
    On average, the interpolated shape points should be approximately equal to num_new_pts.
    First point will be added to close the shape.
    No interpolation if number of new points is less than points in the reduced shape, reduced shape will be returned instead.

    Args:
        shape (list): list of shape point tuples (x, y)
        num_new_pts (int): approx. number of new points

    Returns:
        list: new list of interpolated shape point tuples (x, y)
    """
    # In reduced_shape point list duplicate points are removed (for interpolation).
    reduced_shape = list(dict.fromkeys(shape.copy()))

    # No interpolation if fewer points are given than the number of points present in the reduced_shape.
    if num_new_pts <= len(reduced_shape):
        # Adds first point to close the reduced shape.
        reduced_shape.append(shape[-1])
        return reduced_shape

    interpol_shape = []
    ratio_pts_length = (num_new_pts - len(reduced_shape)) / \
        get_shape_length(reduced_shape)

    # Builds a interpolated shape list from interpolated segments.
    # Number of interpolated points is calculated by segment to shape length ratio.
    for i in range(1, len(reduced_shape)):
        point1 = reduced_shape[i - 1]
        point2 = reduced_shape[i]
        segment_length = get_dist_points(point1, point2)
        num_interpol_points = int(round(ratio_pts_length * segment_length, 0))
        interpol_points = lin_interpolate(point1, point2, num_interpol_points)
        interpol_shape.append(point1)
        interpol_shape.extend(interpol_points)

    # Adds first point to close the reduced shape.
    interpol_shape.append(shape[-1])

    return interpol_shape
