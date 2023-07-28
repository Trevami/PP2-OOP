import pygame
import math
import cmath
from classes.TraceSubsurface import TraceSubsurface
from classes.RotArrow import RotArrow
from classes.Button import Button
from classes.SettingsOverlay import SettingsOverlay
from functions.vectors_and_interpolation import get_vec_screen_pos, lin_interpolate_shape


class ArrowSubsurface(TraceSubsurface):
    def __init__(self, surf: pygame.Surface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(surf, left, top, width, height, **kwargs)
        defaultKwargs = {
            "shape_interpol_pts": 400, # Should be around or higher than the number of arrows.
            "shape": False,
            "arrow_circles": True,
            "trace_length": 3000,
            "surf_color": pygame.Color(25, 22, 20),
            "arrow_color": pygame.Color(80, 80, 80),
            "arrow1_color": pygame.Color(40, 120, 40),
            "cross_color": pygame.Color(80, 80, 80),
            "shape_color": pygame.Color(0, 80, 200),
            "on_surf_item_margin": 20
        }
        kwargs = defaultKwargs | kwargs
        self.on_surf_item_margin = kwargs["on_surf_item_margin"]
        self._arrow_group = pygame.sprite.Group()
        self.shape_points = []
        self.shape_interpol_pts = kwargs["shape_interpol_pts"]
        self.shape = kwargs["shape"]
        self.arrow_circles = kwargs["arrow_circles"]
        self.setting_button = self._create_settings_button()
        self.settigs_overlay = self._create_settings_overlay()
        self.time_factor = self.set_time_factor() # Should be changed
        self.trace_length = kwargs["trace_length"]
        self.surf_color = kwargs["surf_color"]
        self.arrow_color = kwargs["arrow_color"]
        self.arrow1_color = kwargs["arrow1_color"]
        self.cross_color = kwargs["cross_color"]
        self.shape_color = kwargs["shape_color"]
        self.set_time_factor()

    def set_time_factor(self, speed=3):
        # Will be changed in future.
        # Sets time delay.
        # Higher speed values increase the speed of the arrows.
        self.time_factor = 1/30 * speed

    def set_shape(self, shape):
        # Interpolates shape if more than 3 points.
        if len(shape) >= 3:
            self.shape_points = lin_interpolate_shape(shape, self.shape_interpol_pts)
        else:
            self.shape_points = shape

    def set_arrow_palette(self, palette: dict):
        self.arrow_color = palette["arrow_color"]
        self.arrow1_color = palette["arrow1_color"]

    def set_arrow_circles(self, state: bool):
        self.arrow_circles = state
        for arrow in list(self._arrow_group)[1:]:
            arrow.circle = self.arrow_circles

    def create_arrows(self):
        if len(self.shape_points) >= 3:
            # Removes old arrows.
            self.clear_arrows()

            # Calculates arrow init parameters.
            # The var: constant sets the init size (real part) and the angle (imag part) of arrow.
            # The var: exp_mult determines the exp multipliers of Euler's equation.
            exp_mult = 0 # Start point for series generation.
            for i in range(int(self.settigs_overlay.arrow_slider.value)):
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
                    function -= self.surf.get_width() / 2 + self.surf.get_height() / 2 * 1j
                    # Function for calculation of constant c_i (index i) term of arrow:
                    constant += function * cmath.exp(exp_mult * 2 * math.pi * 1j * t) * dt
                
                # Initializes arrow with calculated parameters.
                arrow = RotArrow(
                    constant,
                    exp_mult,
                    color=self.arrow_color,
                    time_factor=self.time_factor,
                    circle=self.arrow_circles
                    )
                self._arrow_group.add(arrow)

            self._update_first_arrow()
    
    def _create_settings_button(self):
        button_width = 35
        button_height = button_width
        return Button(
            self.surf,
            self.on_surf_item_margin,
            self.on_surf_item_margin,
            button_width,
            button_height,
            pressed = False,
            font_type="Segoe UI Symbol",
            font_margin=8,
            text="☰"
        )
    
    def _create_settings_overlay(self):
        return SettingsOverlay(
            self,
            0,
            0,
            self.surf.get_width(),
            self.surf.get_height(),
            show=self.setting_button.pressed
        )
    
    def clear_arrows(self):
        # Deletes all arrows.
        self._arrow_group.empty()

    def update_arrows(self):
        # Updates the arrows and the anchors of all arrows to the vector end of the previous arrow. 
        for i in range(1, len(self._arrow_group)):
            arrow = self._arrow_group.sprites()[i]
            pev_arrow_vec_pos = get_vec_screen_pos(self._arrow_group.sprites()[i - 1])
            arrow.set_anchor(
                ((pev_arrow_vec_pos[0] - arrow.surf.get_width() / 2),
                (pev_arrow_vec_pos[1] - arrow.surf.get_height() / 2))
            )

        # Arrow update:
        for arrow in self._arrow_group:
            arrow.time_factor = self.time_factor
            arrow.update()

    def _update_first_arrow(self):
        # Sets the anchor position to center of ArrowSurface for first arrow.
        self._arrow_group.sprites()[0].set_anchor(
            ((self.surf.get_width() - self._arrow_group.sprites()[0].surf.get_width()) / 2,
            (self.surf.get_height() - self._arrow_group.sprites()[0].surf.get_height()) / 2)
        )
        # Changes color and circle of first arrow.
        self._arrow_group.sprites()[0].color = self.arrow1_color
        self._arrow_group.sprites()[0].circle = False

    def _draw_arrows(self):
        # Draws arrows.
        for arrow in self._arrow_group:
            arrow.draw_update()
            self.surf.blit(arrow.surf, arrow.get_anchor())

    def _draw_trace(self):
        if len(self._arrow_group):
            self.trace.append(get_vec_screen_pos(self._arrow_group.sprites()[-1]))

            if len(self.trace) > self.trace_length:
                self.trace.pop(0)

            if len(self.trace) >= 3:
                pygame.draw.lines(
                    self.surf,
                    self.trace_color,
                    False,
                    self.trace[1:],
                    width=self.trace_width
                )

    def _draw_shape(self):
        # Draws shape
        if len(self.shape_points) >= 3 and self.shape:
            pygame.draw.lines(
                self.surf,
                self.shape_color,
                False,
                self.shape_points,
                width=int(self.trace_width / 2)
            )

    def _draw_setting_button(self):
        self.setting_button.draw_update()

    def _draw_settigs_overlay(self):
        self.settigs_overlay.draw_update()

    def draw_update(self):
        self.clear_surface()
        self.surf.fill(self.surf_color)
        
        self.draw_cross()
        self._draw_shape()
        self._draw_arrows()
        self._draw_trace()
        self._draw_settigs_overlay()
        self._draw_setting_button()