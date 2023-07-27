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
        self.arrow_slider = self._create_arrow_slider()
        self.buttons = self._create_buttons()

    def _create_arrow_slider(self):
        # Sets the margin relative to the ArrowSurface
        slider_margin = self.on_surf_item_margin
        # Sets width and height of the Slider.
        slider_width = self.surf.get_width() - (2 * slider_margin)
        slider_height = 30
        # Creates a slider.
        return Slider(
            self.surf,
            slider_margin,
            (self.surf.get_height() - (slider_margin + slider_height)),
            slider_width,
            slider_height,
            min=10,
            max=200,
            ticks=19,
            start=40,
            text="Arrows",
            type="int"
            )
    
    def _create_buttons(self):
        button_margin = self.on_surf_item_margin
        button_space_margin = self.on_surf_item_margin / 2
        button_width = 35
        button_height = button_width

        shape_toggle_button = Button(
            self.surf,
            (self.surf.get_width() - (button_margin + button_width)),
            button_margin,
            button_width,
            button_height,
            pressed = self.rs_parent.shape
        )

        circle_toggle_button = Button(
            self.surf,
            (self.surf.get_width() - (button_margin + button_width)),
            (button_margin + button_height + button_space_margin),
            button_width,
            button_height,
            pressed = self.rs_parent.arrow_circles
        )

        return {
            "shape_toggle": shape_toggle_button,
            "circle_toggle": circle_toggle_button
        }

    def _draw_slider(self):
        self.arrow_slider.draw_update()
    
    def draw_update(self):
        if self.show:
            self._draw_slider()
            for button in self.buttons.values():
                button.draw_update()