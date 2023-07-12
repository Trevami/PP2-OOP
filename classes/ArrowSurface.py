import pygame
import math
import cmath
from classes.TraceSurface import TraceSurface
from classes.Arrow import RotArrow
from classes.Slider import Slider
from functions.vectors_and_interpolation import get_vec_screen_pos, lin_interpolate_shape

class ArrowSurface(TraceSurface):
    def __init__(self, size, *args, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.arrow_group = pygame.sprite.Group()
        self.arrow_slider = self._create_arrow_slider()
        self.shape_points = []
        self.time_factor = self.set_time_factor() # Should be changed
        self.shape_interpol_pts = 420 # Should be around or higher than the number of arrows.
        self.trace_length = 3000
        self.surf_color = pygame.Color(25, 22, 20)
        self.arrow_color = pygame.Color(80, 80, 80)
        self.arrow1_color = pygame.Color(40, 120, 40)
        self.cross_color = self.arrow_color
        self.shape = True
        self.shape_color = pygame.Color(0, 80, 200)
        self.set_time_factor()

    def set_time_factor(self, speed=3):
        # Will be changed in future.
        # Sets time delay.
        # Higher speed values increase the speed of the arrows.
        self.time_factor = 1/30 * speed

    def create_arrows(self):
        if len(self.shape_points) >= 3:
            # Removes old arrows.
            self.clear_arrows()

            # Calculates arrow init parameters.
            # The var: constant sets the init size (real part) and the angle (imag part) of arrow.
            # The var: exp_mult determines the exp multipliers of Euler's equation.
            exp_mult = 0 # Start point for series generation.
            for i in range(int(self.arrow_slider.value)):
                # Generates a series of exp multipliers: 0, -1, 1, -2, 2 ...
                exp_mult += (-1)**i * -i
                constant = 0
                num_points = len(self.shape_points)
                # Integral approximation with a sum (index k, 0 to num_points):
                # Higher shape point count will increase accuracy.
                for point_k in range(num_points):
                    t = point_k / num_points # Independent variable t for approximation of integral.
                    dt = 1 / num_points # dt term for approximation of integral.
                    # f(t) function, composed of x_pos (real part) and y_pos (imag part) of data point:
                    function = self.shape_points[point_k][0] + self.shape_points[point_k][1] * 1j
                    # Offset position correction for shape center to center of surface:
                    function -= self.get_width() / 2 + self.get_height() / 2 * 1j
                    # Function for calculation of constant c_i (index i) term of arrow:
                    constant += function * cmath.exp(exp_mult * 2 * math.pi * 1j * t) * dt
                
                # Initializes arrow with calculated parameters.
                arrow = RotArrow(constant, exp_mult, 1, 10, True)
                arrow.time_factor = self.time_factor
                self.arrow_group.add(arrow)

            # Sets the anchor position to center of ArrowSurface for first arrow.
            self.arrow_group.sprites()[0].set_anchor(
                (self.get_width() - self.arrow_group.sprites()[0].surf.get_width()) / 2,
                (self.get_height() - self.arrow_group.sprites()[0].surf.get_height()) / 2
            )

    def _create_arrow_slider(self):
        # Sets the margins relative to the ArrowSurface
        slider_margin_sides = 50
        slider_margin_bottom = 20
        # Sets width and height of the Slider.
        slider_width = self.get_width() - (2 * slider_margin_sides)
        slider_height = 30
        # Creates a slider.
        return Slider(
            self,
            slider_margin_sides,
            (self.get_height() - (slider_margin_bottom + slider_height)),
            slider_width,
            slider_height,
            min=10,
            max=210,
            ticks=20,
            start=40,
            text="Arrows",
            type="int"
            )

    def update_arrows(self):
        # Updates the arrows and the anchors of all arrows to the vector end of the previous arrow. 
        for i in range(1, len(self.arrow_group)):
            arrow = self.arrow_group.sprites()[i]
            pev_arrow_vec_pos = get_vec_screen_pos(self.arrow_group.sprites()[i - 1])
            arrow.set_anchor(
                (pev_arrow_vec_pos[0] - arrow.surf.get_width() / 2),
                (pev_arrow_vec_pos[1] - arrow.surf.get_height() / 2)
            )

        # Arrow update:
        for arrow in self.arrow_group:
            arrow.time_factor = self.time_factor
            arrow.update()

    def clear_arrows(self):
        # Deletes all arrows.
        self.arrow_group.empty()

    def set_shape(self, shape):
        # Interpolates shape if more than 3 points.
        if len(shape) >= 3:
            self.shape_points = lin_interpolate_shape(shape, self.shape_interpol_pts)
        else:
            self.shape_points = shape
    
    def set_arrow_palette(self, palette: dict):
        self.arrow_color = palette["arrow_color"]
        self.arrow1_color = palette["arrow1_color"]

    def draw_trace(self):
        pygame.draw.lines(
            self,
            self.trace_color,
            False,
            self.trace[1:],
            width=self.trace_width
        )

    def draw_update(self):
        self.clear_surface()
        self.fill(self.surf_color)
        self.draw_cross()

        # Draws shape (optional):
        if len(self.shape_points) >= 3 and self.shape:
            pygame.draw.lines(
                self,
                self.shape_color,
                False,
                self.shape_points,
                width=int(self.trace_width / 2)
            )

        # Updates arrows.
        for arrow in self.arrow_group:
            arrow.surf.set_colorkey(pygame.Color(255, 255, 255))
            arrow.color = self.arrow_color
            self.blit(arrow.surf, arrow.get_anchor())

        if len(self.arrow_group):
            # Changes first arrow.
            self.arrow_group.sprites()[0].color = self.arrow1_color
            self.arrow_group.sprites()[0].draw_circle = False

            self.trace.append(get_vec_screen_pos(self.arrow_group.sprites()[-1]))

            if len(self.trace) > self.trace_length:
                self.trace.pop(0)

            if len(self.trace) >= 3:
                self.draw_trace()

        # Updates slider.
        slider = self.arrow_slider
        slider.draw_slider()