from classes.RectSubsurface import RectSubsurface
from classes.Slider import Slider
from classes.Button import Button


class SettingsOverlay(RectSubsurface):
    def __init__(self, rs_parent: RectSubsurface, left: float, top: float, width: float, height: float, **kwargs):
        super().__init__(rs_parent.surf, left, top, width, height)
        defaultKwargs = {
            "show": False,
            "on_surf_item_margin": 20
        }
        kwargs = defaultKwargs | kwargs
        self.show = kwargs["show"]
        self.rs_parent = rs_parent
        self.on_surf_item_margin = kwargs["on_surf_item_margin"]
        self._slider_height = 30
        self.arrow_slider = self._create_arrow_slider()
        self.speed_slider = self._create_speed_slider()
        self.buttons = self._create_buttons()

    def _create_arrow_slider(self):
        # Sets the margin relative to the ArrowSurface
        slider_margin = self.on_surf_item_margin
        # Sets width and height of the Slider.
        slider_width = self.surf.get_width() - (2 * slider_margin)
        # Creates a slider.
        return Slider(
            self.surf,
            slider_margin,
            (self.surf.get_height() - (slider_margin + self._slider_height)),
            slider_width,
            self._slider_height,
            min=2,
            max=200,
            ticks=198,
            start=40,
            text="Arrows",
            type="int"
        )
    
    def _create_speed_slider(self):
        # Sets the margin relative to the ArrowSurface
        slider_margin = self.on_surf_item_margin
        # Sets width and height of the Slider.
        slider_width = self.surf.get_width() - (2 * slider_margin)
        # Creates a slider.
        return Slider(
            self.surf,
            slider_margin,
            (self.surf.get_height() - (slider_margin + slider_margin / 2 + self._slider_height * 2)),
            slider_width,
            self._slider_height,
            min=1,
            max=100,
            ticks=20,
            start=50,
            text="Speed ",
            type="int"
        )

    def _create_buttons(self):
        button_margin = self.on_surf_item_margin
        button_space_margin = self.on_surf_item_margin / 2
        button_width = 35
        button_height = button_width

        settings_toggle_button = Button(
            self.surf,
            self.on_surf_item_margin,
            self.on_surf_item_margin,
            button_width,
            button_height,
            pressed = self.show,
            font_type="Segoe UI Symbol",
            font_margin=8,
            text="☰"
        )

        shape_toggle_button = Button(
            self.surf,
            (self.surf.get_width() - (button_margin + button_width)),
            button_margin,
            button_width,
            button_height,
            pressed=self.rs_parent.shape,
            text="S"
        )

        circle_toggle_button = Button(
            self.surf,
            (self.surf.get_width() - (button_margin + button_width)),
            (button_margin + button_height + button_space_margin),
            button_width,
            button_height,
            pressed=self.rs_parent.arrow_circles,
            text="C"
        )

        return {
            "settings_toggle": settings_toggle_button,
            "shape_toggle": shape_toggle_button,
            "circle_toggle": circle_toggle_button
        }

    def _draw_sliders(self):
        self.arrow_slider.draw_update()
        self.speed_slider.draw_update()

    def draw_update(self):
        if self.show:
            self._draw_sliders()
            for button in self.buttons.values():
                button.draw_update()
        else:
            self.buttons["settings_toggle"].draw_update()